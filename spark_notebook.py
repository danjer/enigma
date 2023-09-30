import pyspark.sql.functions as F
from typing import List
from enigma._crack import get_possible_settings, PlugBoardResolver, InvalidSettings
from enigma._enigma import Enigma
from pyspark.sql.session import SparkSession
from pyspark.sql import Row
from functools import partial

NOT_RESOLVABLE = "NOT_RESOLVABLE"


def translate_with_settings(rotor_types, reflector_type, ring_settings, plugboard_pairs, text):
    enigma = Enigma(rotor_types=rotor_types, reflector_type=reflector_type, ring_settings=ring_settings,
                    plugboard_pairs=plugboard_pairs)
    return enigma.encrypt(text)


def score_setting(rotor_types, reflector_type, ring_settings, plugboard_pairs, cypher, crib) -> int:
    output = translate_with_settings(rotor_types, reflector_type, ring_settings, plugboard_pairs, cypher)
    return len([l for l, r in zip(output, crib) if l == r])


def resolve_plugboard_possibilities(rotor_types, reflector_type, ring_settings, cypher, crib) -> List[str]:
    plugboard_resolver = PlugBoardResolver(crib, cypher, rotor_types, reflector_type, ring_settings)
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

naive_score_function = partial(score_setting, cypher=cypher, crib=crib, plugboard_pairs=None)
score_function = partial(score_setting, cypher=cypher, crib=crib)
resolve_plugboard_function = partial(resolve_plugboard_possibilities, cypher=cypher, crib=crib)

rdd = spark.sparkContext.parallelize(
    [(v, Row(rotor_types=v[0], reflector_type=v[1], ring_settings=v[2])) for v in get_possible_settings()], 2)

# Get scores for every rotor_settings without any plugboard configuration.
rdd = rdd.mapValues(
    lambda r: Row(rotor_types=r.rotor_types, reflector_type=r.reflector_type, ring_settings=r.ring_settings,
                  naive_score=naive_score_function(r.rotor_types, r.reflector_type, r.ring_settings)))

# only consider the best naive rotor settings
rdd = spark.sparkContext.parallelize(rdd.top(100, key=lambda r: r[1].naive_score))

rdd = rdd.flatMapValues(
    lambda r: [Row(rotor_types=r.rotor_types,
                   reflector_type=r.reflector_type,
                   ring_settings=r.ring_settings,
                   plugboard_pairs=pp) for pp in
               resolve_plugboard_function(r.rotor_types, r.reflector_type, r.ring_settings)])

rdd = rdd.filter(lambda x: x[1].plugboard_pairs != NOT_RESOLVABLE)

rdd = rdd.mapValues(lambda r: Row(rotor_types=r.rotor_types,
                                  reflector_type=r.reflector_type,
                                  ring_settings=r.ring_settings,
                                  plugboard_pairs=r.plugboard_pairs,
                                  score=score_function(r.rotor_types, r.reflector_type, r.ring_settings,
                                                       r.plugboard_pairs),
                                  translated=translate_with_settings(r.rotor_types, r.reflector_type, r.ring_settings,
                                                                     r.plugboard_pairs, cypher)

                                  ))

df = rdd.map(lambda v: v[1]).toDF()
df = df.filter(F.col('plugboard_pairs') != NOT_RESOLVABLE)
df = df.orderBy(F.col('score'), ascending=False)
df.show()
