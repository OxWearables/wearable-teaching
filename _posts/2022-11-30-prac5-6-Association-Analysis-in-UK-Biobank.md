---
layout: post
---

## Introduction 

Practical sessions on Thursday morning and Friday morning will focus on how accelerometer-derived phenotypes can be used in UK Biobank to generate epidemiological insights. 

The session on Thursday focuses on **accessing** the data. We will understand some of the non-accelerometer data available in UK Biobank, meet the [UK Biobank Research Analysis Platform](https://www.ukbiobank.ac.uk/enable-your-research/research-analysis-platform) and use it to prepare data for analysis. 

The session on Friday focuses on **running an epidemiological analysis** using data from UK Biobank. 

Both sessions use [this demo pipeline]([https://github.com/OxWearables/rap_wearables](https://github.com/OxWearables/rap_wearables/tree/cdt_dec_2022)), with Thursday's session focussing on [notebook 1](https://github.com/OxWearables/rap_wearables/blob/main/1_Extract_Data.ipynb) and Friday's on notebooks 2-4.

**Tutors:** Aidan Acquah, Alaina Shreves, Rosemary Walmsley


## Information Governance and Security

When working with participant data, good Information Governance/Security is essential. Work with data **on the Research Analysis Platform only**. Do not download data onto your machine. Watch out for accidental data download e.g. a Jupyter notebook may inadvertently contain data (e.g. from printing parts of the data).  

## Practicalities: getting the notebooks onto the UK Biobank Research Analysis Platform

The UK Biobank Research Analysis Platform has permanent storage. When you are running JupyterLab (or RStudio), you are temporarily running a cloud computer that has some temporary storage associated with it. You can transfer things from permanent storage to temporary storage and back again. **Important:** at the end of a session, before terminating your cloud computer, you need to make sure anything you need from the temporary storage is transferred over to permanent storage. If not, it will be gone! 

There are different ways you could get the practical materials from GitHub onto the Research Analysis Platform. Here's one: 

I. Launch JupyterLab + Spark (as you will need for the Thursday practicals) 

II. Open a Terminal instance from JupyterLab (File > New > Terminal) 

III. Clone the repository by running: 
```shell
$ git clone https://github.com/OxWearables/rap_wearables.git # need to use https clone as ssh clone doesn't seem to be set up
```

IV. Note that this has put the repository into *temporary storage only*. If you want to be able to access it after the session, you'll still need to upload it to permanent storage. 

V. To work with the repository, change the directory into the repository and check out the relevant branch: 

```shell
$ cd rap_wearables
$ git checkout cdt_dec_2022 # This branch has some minor changes relative to main making it more suitable for our work this week 
```

VI. You can now run notebooks from the repository and edit them as you like. 

VII. At the end of the session, you can upload to permanent storage by running (again in the terminal): 
```shell
$ dx upload -r rap_wearables --dest users/Rosemary_Walmsley32/ # Remember to change my username to yours! Also don't miss the trailing slash. 
# dx is a command line client produced by DNANexus
```

Alternatively, if you already have things in permanent storage (e.g. having previously run through the steps above), you can download them to your temporary instance using: 

```shell
$ dx download -r users/Rosemary_Walmsley32/rap_wearables # again change the file path as appropriate
```


## Reading and useful links

- Documentation for the Research Analysis Platform: https://dnanexus.gitbook.io/uk-biobank-rap/
- The DNANexus community: https://community.dnanexus.com/s/ (useful for troubleshooting)
