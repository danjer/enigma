import pyspark.sql.functions as F
from typing import List
from enigma._crack import get_possible_settings, PlugBoardResolver, InvalidSettings
from enigma._enigma import Enigma
from pyspark.sql.session import SparkSession
from pyspark.sql import Row
from functools import partial

NOT_RESOLVABLE = "NOT_RESOLVABLE"


def score_setting(rotor_settings, cypher, crib) -> int:
    e = Enigma(*rotor_settings)
    return len([l for l, r in zip(e.encrypt(cypher), crib) if l == r])


def resolve_plugboard_possibilities(rotor_settings, cypher, crib) -> List[str]:
    plugboard_resolver = PlugBoardResolver(crib, cypher, rotor_settings)
    try:
        plugboard_resolver.eliminate_pairs()
    except InvalidSettings:
        return [NOT_RESOLVABLE]
    if plugboard_resolver.get_remaining() > 1000:
        return [NOT_RESOLVABLE]
    else:
        return plugboard_resolver.get_remaining_pairs()


spark = SparkSession.builder.getOrCreate()

e = Enigma(rotor_types="II,III,I", ring_settings="I,A,A", plugboard_pairs="CU,DL,EP,KN,MO,XZ")
crib = "WettervorhersageXXXfurxdiexRegionXXXOstXXXMoskau".upper()
cypher = e.encrypt(crib)

score_function = partial(score_setting, cypher=cypher, crib=crib)
resolve_plugboard_function = partial(resolve_plugboard_possibilities, cypher=cypher, crib=crib)

# Get scores for every rotor_settings without any plugboard configuration.
rdd = spark.sparkContext.parallelize([(v, v) for v in get_possible_settings()], 2)
rdd = rdd.mapValues(lambda r: Row(rotor_settings=r, score=score_function(r)))

# only consider the best naive rotor settings
rdd = spark.sparkContext.parallelize(rdd.top(100, key=lambda r: r[1].score))
rdd = rdd.flatMapValues(
    lambda r: [Row(rotor_settings=r.rotor_settings, score=r.score,
                   plugboard_pairs=pp) for pp in resolve_plugboard_function(r.rotor_settings)])

df = rdd.map(lambda v: v[1]).toDF()
df = df.filter(F.col('plugboard_pairs') != NOT_RESOLVABLE)
df.show()
