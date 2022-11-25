---
layout: post
---

* This will become a table of contents (this text will be scrapped).
{:toc}


# Camera image annotation
In this practical, you will learn how to process and annotate the camera data you have been collecting over the past few hours.

# 0. Data extraction

We now want to extract the raw images from your camera. We'll perform the following from the `utilities` folder within `oxford-wearable-camera-browser`. Change directory and start the virtual environment we set up earlier this morning.
```shell
$ cd ~/oxford-wearable-camera-browser/utilities
$ source .venv/bin/activate
```
Now plug in your camera. To download the photos:
```shell 
$ python autographer.py --download True --destDir ~/OxfordImageBrowser/images/<your_name>
```
To delete the photos on the device, run:
```shell 
$ python autographer.py --delete True
```

Safely disconnect the device and return it to your tutor. If you open the folder (`~/OxfordImageBrowser/images/<your_name>`) where you extracted the images to, you can browse through the images and delete any that you wish to. 

In order for the camera browser to work, we need to create thumbnail sized version of your photos. To do this, install `imagemagick`:
```shell
$ brew install imagemagick
```
Then to resize: (this could take about 10 minutes to run)
```shell
$ cd ~/oxford-wearable-camera-browser/utilities
$ bash create_thumbnails.sh ~/OxfordImageBrowser/images/<your_name>/
```


###  Folder structure
We will now walk through how the browser reads in the images for annotation. Our setup has created a new directory in your root folder at `/Users/{yourName}/OxfordImageBrowser/`, this further contains 3 folders: `annotations`,`images`, `schema`.

* `images/`

    This is where you store images which you want to annotate. You should have a folder structure like this. You should move the reference images to the `images` folder with a similar directory structure.

    ```shell
        /Users/<yourName>/OxfordImageBrowser/images/
            participantID/
                AAAAAAAAA_BBBBBB_YYYYMMDD_HHMMSSE.JPG
                ...
    ```

* `schema/`

    This is where you will store csv files which specify your annotation schemes.

    You should have 3 schema .csv files (7class, annotation, social), along with a template for free text annotation. For the purpose of these practicals, do not edit any of these files except for `free_text.csv`.

    Should you want to define your own schema, simply copy one of the existing ones and add/remove rows as you see fit. You can use either a text editor (Notepad), or Excel. If using Excel make sure to save as .csv filetype, as .xls files will not be recognised.

    Your annotation training will focus on the schema `annotation.csv`, which is a specific set of activities based on the [Compendium of Physical Activities](https://sites.google.com/site/compendiumofphysicalactivities/home). Have a browse at this file to check the available activity annotations. You should move the schema you want to use into `OxfordImageBrowser/schema`. Template schema files can be found at `practicals/assets/schema`.


* `annotation/`

    This is where the Browser outputs your annotation files by default. A sub-folder will be created for each participant found in `images/`.




## 4.2 Annotating a reference dataset

Now you can open `OxfordImageBrowser` and annotate the reference data.

* Start the image browser.

```
$ cd ~/Development/oxford-wearable-camera-browser/
$ npm start
```

* Click on the leftmost participant selection icon. You should see it reflecting the updated list of test participants.

* For each participant:

    * Select the participant.

    * Select the annotation scheme `annotation.csv`

    * Annotate all images belonging to the participant (see instructions just below)

    * When finished, check the top bar to ensure annotation is 100% complete.

    * Check that the annotation CSV file has been automatically saved to the default location (inside `~/OxfordImageBrowser/annotations/<your_name>/`); If not, manually save the annotations by clicking the download button.


### Annotating images.
All previous annotators of the CAPTURE-24 dataset had to go through extensive training - annotating at least 8 test subjects - before they can go on to annotate other data. We will not subject you to that experience! However, today you will get a taste of this by annotating your own data. To start with, please go through parts C & D of [this supplementary document](https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-018-26174-1/MediaObjects/41598_2018_26174_MOESM2_ESM.docx) from [this paper](https://www.nature.com/articles/s41598-018-26174-1) to understand how you should annotate the images.

The overall flow is [described in great detail here](https://github.com/activityMonitoring/oxford-wearable-camera-browser) where the essential elements are to:

![](./assets/figs/EDNitOT.png)

1. Divide up the images into different events/activities by clicking on the timeline above the images: I) To move event boundaries, click and drag the circles. II) For instance this split is where I think the participant has started locking up their bike.

2. Look at consecutive images to determine the most suitable annotation for each image sub-sequence. You can also make use of the search bar if you are unsure where the annotations are located in the hierarchy.

3. Pull the selected annotation onto the image(s). To change an activity annotation simply drag another annotation over it.


After annotating the data using the scheme `annotation.csv`, please perform the following annotation exercises.

<!-- 1. `7class.csv`: similar to what you did with `annotation.csv`. -->

1. `social.csv`: annotate events which you think are of a social nature (e.g. having lunch with friends) versus those which are not. This schema may install as a blank .csv. To fix this, open the social.csv file and add your own categories. For example, social, non-social, social-with-one, social-with-2plus, etc.

2. `free_text.csv`: In the previous exercises, you have been confined by the definition of the annotations to define 'events' / 'activities'. In this case, could you come up with your own description or annotations and divide up the image timeline according to what feels most natural to you? You would need to put your event annotations / descriptions into a CSV file, and drag these to annotate your events. The current `free_text.csv` has been provided as an example but be creative.

3. Write a 1-liner summary for each day. Save this as a `per_day.csv` file where you have one line per row. Divide up your time line

At the end of these exercises, you should have 4 annotation CSV files saved in your `OxfordImageBrowser/annotation/me` directory.

<!-- browser_dir = '/Users/<yourName>/OxfordImageBrowser/annotation/me/' -->

Copy the `my-annotations.csv` file over to your `~/practicals/data/` folder.



<!-- ### Uncodeable Activities

In your resulting time-series file, you might notice that some of your annotations are 'uncodeable'. Here are some ways to fix this.

* Sleep

Do the following if you want your annotated time series to have 'sleep' events.

Open your annotations file at `~/wearable-teaching/practicals/data/my-annotations.csv` and manually change the annotation of the events you believe correspond to your sleeping hours into `7030 sleeping`.

* Other Events

Do the following if you notice that there are other events in your time series which you have annotated but appears to be `uncodeable` in your plot.

Open the file at `~/wearable-teaching/practicals/data/prac3_process_camera/annotation-label-dictionary.csv` and manually append the table.

For example, 'leisure;recreation;outdoor;15533 rock or mountain climbing' is not currently in the annotation-label dictionary. Append the table, putting 'leisure;recreation;outdoor;15533 rock or mountain climbing' in the 'annotation' column, and a category which you feel is appropriate under the 'label:Doherty2018' column (in this case I've assigned the latter as moderate):

![](./assets/figs/add_uncodeable.png) -->




# 5. (Optional) Challenge: Cross-check your own annotations with others
Try to understand if you can use [this](https://github.com/activityMonitoring/oxford-wearable-camera-browser/blob/master/kappaScoring.py) to compare your annotations with another student. To run this script, you will first need to install four depedencies:

```shell
$ pip3 install argparse
$ pip3 install numpy
$ pip3 install pandas
$ pip3 install -U scikit-learn
```

Then generate the list of image file names in [this](https://github.com/activityMonitoring/oxford-wearable-camera-browser/blob/master/training/train1-fileList.txt) format and store this as `cdt-fileList.txt` under the `~/oxford-wearable-camera-browser/training` folder. Move your own annotation to the same place and rename it as `cdt-ref.csv`.

Now go a get another annotation file from your friend, you can run the comparison script via:
```shell
$ python kappaScoring.py /..path../annotation.csv
```

To generate the file list, you can use this Python script:
```python
import os 
import glob

path2gen = '/Users/hangy/plots'
file_list = glob.glob(os.path.join(path2gen, '*.JPG'))

with open('file.txt', 'w') as f:
    for item in file_list:
        txt2write = item.split('/')[-1]
        print(txt2write)
        f.write("%s\n" % txt2write)
```
When you are done, let your tutor know what your kappa score is.


# Matching with accelerometer timings? 