# Cracking the Enigma Using Apache Spark

The Enigma machine was a configurable device used by the Germans during World War II to encrypt confidential
information. Although Nazi Germany placed great faith in the capabilities of the machine, it suffered from a few design
flaws that the Allies managed to exploit, enabling them to read secret information. The story of deciphering the Enigma
has been depicted in the film "The Imitation Game."

In this post, I will demonstrate how I cracked the Enigma machine using Apache Spark. This framework is widely used in
big data analysis because it allows for distributed calculations and storage of data. This way, one can execute a
massive amount of calculations on different machines, which can dramatically speed up the overall execution time. The
process of cracking the Enigma involves several number crunching steps that can be executed in parallel. Because of
this, Spark is an ideal tool to speed up the process.

## The Overall Approach for Cracking the Enigma

In this post, I won't go into detail about the underlying workings of the Enigma machine or the algorithms that can be
used to crack it. In short, the Enigma machine is a device that scrambles input letters to produce different output
letters. With each button press, the mapping changes. This, combined with the fact that the Enigma machine could be
configured in 158,962,555,217,826,360,000 different ways, led the Germans to believe that it was uncrackable. However,
the fact that each input letter differs from the output makes it relatively easy to align a "crib," a short known piece
of the original text, with the encrypted text. Numberphile has some
informative [videos](https://www.youtube.com/watch?v=G2_Q9FoD-oQ) about the Enigma in which they explain the algorithms
involved in breaking the Enigma. I implemented these algorithms and an Enigma emulator in a separate Python package,
which I used in a standalone script to break the Enigma with parallel computation on Databricks (sort of Spark as a
service). All the code for this project is available on Github.

### Setting up the infrastructure
In this project I use Databricks as the Spark provider. To set up the Databricks workspace in azure cloud I use
[Terraform](https://www.terraform.io/). Assuming that terraform is installed, enter the terraform folder and run:
```commandline
terraform init
terraform apply
```
After the whole infrastructure is created, which will probably take a few minutes, you can navigate to
the databricks workspace by clicking on the URL that is outputed in the terminal.
The wokspace if preconfigured with a single node cluster with the engima-emulator installed. Also, the notebook
that I w