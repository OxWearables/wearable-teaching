---
layout: post
---

* This will become a table of contents (this text will be scrapped).
{:toc}


# Camera image annotation
In this practical, you will learn how to process and annotate the camera data you have been collecting over the past few hours.

# 0. Oxford wearable browser
Start by installing the Oxford wearable camera browser to your home folder. You can find more details about the camera browser on [GitHub](https://github.com/activityMonitoring/oxford-wearable-camera-browser). In essence, it is a graphical user interface that allows researchers to annotate camera logger data. Note, this browser is currently in the process of being updated, so do not be surprised if there are dependency warnings in this legacy version. 

Start by installing node.js on your iMac:
```shell 
$ brew install node
```
Once node.js has been installed, clone the camera browser repository into your home directory:
```shell
$ cd ~
$ git clone https://github.com/OxWearables/oxford-wearable-camera-browser.git
```
Install the relevant dependencies, and ignore the dependency warnings.
```
$ cd oxford-wearable-camera-browser
$ npm install  
```
Finally, you can run the camera browser as follows:
```
$ npm start
```
It is import that you run `npm start` so that it sets up a folder called `OxfordImageBrowser`, which is where you will later add your camera data to. However, the browser does not work properly because we haven't added data or schemas to the folder yet, which we will do shortly. You can exit the app by typing `control+c` in the terminal. Let us know if you have any issues here!

# 1. Data extraction

We now want to extract the raw images from your camera and get them into a format that can be used by the Oxford Image Browser.

We start by returning to the `~/practicals/scripts` directory. We will again use `autographer.py` to download data from the camera.

```shell
$ cd ~/practicals/scripts
$ source .venv/bin/activate
```
Now plug in your camera. To download the photos, run:
```shell 
$ python autographer.py --download True --destDir ~/OxfordImageBrowser/images/<your name>
```
To delete the photos on the device, run:
```shell 
$ python autographer.py --delete True
```

Safely disconnect the device and return it to your tutor. If you open the folder (`~/OxfordImageBrowser/images/<your_name>`) where you extracted the images to, you can browse through the images and delete any that you wish to. 

In order for the camera browser to work, we need to create thumbnail sized version of your photos. First install `pillow`, which is used for the image processing. Assuming you are still within the virtual environment in the `~/practicals/scripts` folder, run:

```shell
$ pip install pillow
$ python create_thumbnails.py --root ~/OxfordImageBrowser/images/
```
We should now have the following directory structure in `~/OxfordImageBrowser/`:

- `images/`

    This is where you store images which you want to annotate.

    ```shell
        /Users/<yourName>/OxfordImageBrowser/images/
            <your name>/
                AAAAAAAAA_BBBBBB_YYYYMMDD_HHMMSSE.JPG
                ...
                medium/
                    AAAAAAAAA_BBBBBB_YYYYMMDD_HHMMSSE.JPG
                    ...
                thumbnail/
                    AAAAAAAAA_BBBBBB_YYYYMMDD_HHMMSSE.JPG
                    ...
    ```

* `schema/`

    This is where you will store csv files which specify your annotation schemes.

    You should have 4 schema .csv files (7class, annotation, free_text and social), of which social and free_text are currently blank. We will later edit these to define our own schema.

    Your annotation training will focus on the schema `annotation.csv`, which is a specific set of activities based on the [Compendium of Physical Activities](https://sites.google.com/site/compendiumofphysicalactivities/home). Have a browse through this file to check the available activity annotations.

* `annotation/`

    This is where the browser outputs your annotation files by default. A sub-folder will be created for each participant found in `images/`.



# 2. Annotating your data

Now we can begin to annotate our own data. 

```
$ cd ~/oxford-wearable-camera-browser/
$ npm start
```

At this stage, you should see your name pop up on the left-most panel. If you click on it, you should see you data load to the browser area.

Now, select the annotation scheme `annotation.csv`. At this stage, it is worth explaining the annotation process in more detail. 

All previous annotators of the CAPTURE-24 dataset had to go through extensive training - annotating at least 8 test subjects - before they can go on to annotate other data. We will not subject you to that experience! However, today you will get a taste of this by annotating your own data. To start with, please go through parts C & D of [this supplementary document](https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-018-26174-1/MediaObjects/41598_2018_26174_MOESM2_ESM.docx) from [this paper](https://www.nature.com/articles/s41598-018-26174-1) to understand how you should annotate the images.

The overall flow is [described in great detail here](https://github.com/OxWearables/oxford-wearable-camera-browser) where the essential elements are to:

![](./assets/figs/EDNitOT.png)

1. Divide up the images into different events/activities by clicking on the timeline above the images: I) To move event boundaries, click and drag the circles. II) For instance this split is where I think the participant has started locking up their bike.

2. Look at consecutive images to determine the most suitable annotation for each image sub-sequence. You can also make use of the search bar if you are unsure where the annotations are located in the hierarchy.

3. Pull the selected annotation onto the image(s). To change an activity annotation simply drag another annotation over it.

Once you have finished annotating your data, export the annotations to a .csv file (inside `~/OxfordImageBrowser/annotations/<your_name>/`). This should happen automatically, but you can always do this manually by clicking on the `download annotation` button.

After annotating the data using the scheme `annotation.csv`, please perform the following annotation exercises.

<!-- 1. `7class.csv`: similar to what you did with `annotation.csv`. -->

1. `social.csv`: annotate events which you think are of a social nature (e.g. having lunch with friends) versus those which are not. Open the social.csv file and add your own categories. For example, social, non-social, social-with-one, social-with-2plus, etc.

2. `free_text.csv`: In the previous exercises, you have been confined by the definition of the annotations to define 'events' / 'activities'. In this case, could you come up with your own description or annotations and divide up the image timeline according to what feels most natural to you? You would need to put your event annotations / descriptions into a CSV file, and drag these to annotate your events. The current `free_text.csv` has been provided as an example but be creative.


# (Optional) Challenge: Cross-check your own annotations with others
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


# Matching with accelerometer timings
Another direction is to develop code that matches you accelerometer data with your camera annotations. 
Importantly, check which annotation scheme is used in the later notebooks (probably 7class?).