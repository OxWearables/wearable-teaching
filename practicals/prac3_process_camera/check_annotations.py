import matplotlib
matplotlib.use('Agg')
import argparse
from datetime import datetime, timedelta, time
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import itertools
from sklearn.metrics import confusion_matrix

LABEL_DICTIONARY = 'label-dictionary.csv'

DOHERTY_NatComms_DICT_COL = 'label:NatCommsSimplified'
DOHERTY_NatComms_COLOURS = {'sleep':'blue', 'sedentary':'red',
    'tasks-light':'darkorange', 'walking':'lightgreen', 'moderate':'green'}
DOHERTY_NatComms_LABELS = list(DOHERTY_NatComms_COLOURS.keys())

WILLETS_SciReports_DICT_COL = 'Slabel:SciReportsSimplified'
WILLETS_SciReports_COLOURS = {'sleep':'blue', 'sit.stand':'red',
    'vehicle':'darkorange', 'walking':'lightgreen', 'mixed':'green',
    'bicycling':'purple'}
WILLETS_SciReports_LABELS = list(WILLETS_SciReports_COLOURS.keys())

IMPUTED_COLOR = '#fafc6f'  # yellow
UNCODEABLE_COLOR = '#d3d3d3' # lightgray
BACKGROUND_COLOR = '#d3d3d3' # lightgray


def buildLabelDict(labelDictCSV, labelDictCol):
    df = pd.read_csv(labelDictCSV, usecols=['annotation', labelDictCol])
    labelDict = {row['annotation']:row[labelDictCol] for i,row in df.iterrows()}
    return labelDict


def fixTsData(tsData):
    """ Parse column name containing metadata to infer time, create time index and rename the column """

    meta = tsData.columns[0]  # this column name contains the period and sample rate
    _, startDate, endDate, _ = meta.split(' - ')
    sampleRate = meta.split("sampleRate = ")[1].split(" ")[0]

    tsData.index = pd.date_range(start=startDate, end=endDate, freq=str(sampleRate) + 's')
    tsData.rename({meta:'acceleration'}, axis='columns', inplace=True)  # rename the verbose column


def annotateTsData(tsData, annoData, labelDict):
    tsData['annotation'] = 'undefined'
    # tsData['annotation_label'] = 'undefined'

    for i, row in annoData.iterrows():
        start, end = row['startTime'].tz_localize(None), row['endTime'].tz_localize(None)
        label = labelDict.get(row['annotation'], 'uncodeable')
        tsData.loc[(tsData.index > start) & (tsData.index < end), 'annotation'] = label
        # tsData.loc[(tsData.index > start) & (tsData.index < end), 'annotation_label'] = label


def gatherPredictionLabels(tsData, labels):
    tsData['prediction'] = 'undefined'
    tsData.loc[tsData['imputed'] == 1, 'prediction'] = 'imputed'
    for label in labels:
        tsData.loc[(tsData[label] > 0) & (tsData['imputed'] == 0), 'prediction'] = label


def formatXYaxes(ax, day, ymax, ymin):
    # run gridlines for each hour bar
    ax.get_xaxis().grid(True, which='major', color='grey', alpha=0.5)
    ax.get_xaxis().grid(True, which='minor', color='grey', alpha=0.25)
    # set x and y-axes
    ax.set_xlim((datetime.combine(day,time(0, 0, 0, 0)),
        datetime.combine(day + timedelta(days=1), time(0, 0, 0, 0))))
    ax.set_xticks(pd.date_range(start=datetime.combine(day,time(0, 0, 0, 0)),
        end=datetime.combine(day + timedelta(days=1), time(0, 0, 0, 0)),
        freq='4H'))
    ax.set_xticks(pd.date_range(start=datetime.combine(day,time(0, 0, 0, 0)),
        end=datetime.combine(day + timedelta(days=1), time(0, 0, 0, 0)),
        freq='1H'), minor=True)
    ax.set_ylim((ymin, ymax))
    ax.get_yaxis().set_ticks([]) # hide y-axis lables
    # make border less harsh between subplots
    ax.spines['top'].set_color(BACKGROUND_COLOR)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # set background colour to lightgray
    ax.set_facecolor(BACKGROUND_COLOR)


def splitByTimeGap(group, seconds=30):
    subgroupIDs = (group.index.to_series().diff() > timedelta(seconds=seconds)).cumsum()
    subgroups = group.groupby(by=subgroupIDs)
    return subgroups


def confusionMatrix(tsData, labels, normalize=False):
    tsData = tsData.loc[tsData['annotation'] != 'undefined']
    y_true = tsData['annotation'].values
    y_pred = tsData['prediction'].values

    # Compute confusion matrix -- include 'uncodeable' & 'imputed'
    cmLabels = labels + ['uncodeable', 'imputed']
    cm = confusion_matrix(y_true, y_pred, labels=cmLabels)
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    return cm, cmLabels


def plotTimeSeries(tsData, labels, labelColors=None, plotFile='sample'):
    convert_date = np.vectorize(lambda day, x: matplotlib.dates.date2num(datetime.combine(day, x)))

    groups = tsData.groupby(by=tsData.index.date)

    ndays = len(groups)
    nrows = 3*ndays + 1  # ndays x (prediction + annotation + spacing) + legend
    fig = plt.figure(figsize=(10,nrows), dpi=200)
    gs = fig.add_gridspec(nrows=nrows, ncols=1, height_ratios=[2, 2, 1]*ndays+[2])
    axes = []
    for i in range(nrows):
        if (i+1) % 3 == 0: continue  # do not add the axis corresp. to the spacing
        axes.append(fig.add_subplot(gs[i]))

    if labelColors is None:
        color_cycle = itertools.cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])
        labelColors = dict(zip(labels, color_cycle))
    colors = [labelColors[l] for l in labels]

    ymin = tsData['acceleration'].min()
    ymax = tsData['acceleration'].max()

    for i, (day, group) in enumerate(groups):

        axPred, axAnno = axes[2*i], axes[2*i+1]

        # plot acceleration
        t = convert_date(day, group.index.time)
        axPred.plot(t, group['acceleration'], c='k')

        # plot predicted
        ys = [(group['prediction'] == l).astype('int') * ymax for l in labels]
        axPred.stackplot(t, ys, colors=colors, alpha=.5, edgecolor='none')
        axPred.fill_between(t, (group['prediction'] == 'imputed').astype('int') * ymax,
            facecolor=IMPUTED_COLOR)

        # plot annotated
        ys = [(group['annotation'] == l).astype('int') * ymax for l in labels]
        axAnno.stackplot(t, ys, colors=colors, alpha=.5, edgecolor='none')
        axAnno.fill_between(t, (group['annotation']=='uncodeable').astype('int') * ymax,
            facecolor=UNCODEABLE_COLOR, hatch='//')

        axPred.set_ylabel('predicted', fontsize='x-small')
        axAnno.set_ylabel('annotated', fontsize='x-small')
        formatXYaxes(axPred, day, ymax, ymin)
        formatXYaxes(axAnno, day, ymax, ymin)
        # add date to left hand side of each day's activity plot
        axPred.set_title(
            day.strftime("%A,\n%d %B"), weight='bold',
            x=-.2, y=-.3,
            horizontalalignment='left',
            verticalalignment='bottom',
            rotation='horizontal',
            transform=axPred.transAxes,
            fontsize='medium',
            color='k'
        )

    # legends
    axes[-1].axis('off')
    # create a 'patch' for each legend entry
    legend_patches = []
    legend_patches.append(mlines.Line2D([], [], color='k', label='acceleration'))
    legend_patches.append(mpatches.Patch(facecolor=IMPUTED_COLOR, label='imputed'))
    legend_patches.append(mpatches.Patch(facecolor=UNCODEABLE_COLOR, hatch='//', label='uncodeable'))
    # create legend entry for each label
    for label in labels:
        legend_patches.append(mpatches.Patch(facecolor=labelColors[label], label=label, alpha=0.5))
    # create overall legend
    axes[-1].legend(handles=legend_patches, bbox_to_anchor=(0., 0., 1., 1.),
        loc='center', ncol=min(4,len(legend_patches)), mode="best",
        borderaxespad=0, framealpha=0.6, frameon=True, fancybox=True)
    # remove legend border
    axes[-1].spines['left'].set_visible(False)
    axes[-1].spines['right'].set_visible(False)
    axes[-1].spines['top'].set_visible(False)
    axes[-1].spines['bottom'].set_visible(False)

    # format x-axis to show hours
    fig.autofmt_xdate()
    # add hour labels to top of plot
    hours2Display = range(0, 24, 4)
    hrLabels = [(str(hr) + 'am') if hr<=12 else (str(hr-12) + 'pm') for hr in hours2Display]
    axes[0].set_xticklabels(hrLabels)
    axes[0].tick_params(labelbottom=False, labeltop=True, labelleft=False)

    fig.savefig(plotFile, dpi=200, bbox_inches='tight')
    print('Timeseries plot file:', plotFile)


def plotConfusionMatrix(cm, cmLabels, title=None, plotFile='sample'):
    """ https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html """

    fig, ax = plt.subplots()
    ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=cmLabels, yticklabels=cmLabels,
           ylabel='camera annotation',
           xlabel='model prediction')
    if title is not None: ax.set_title(title)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if np.issubdtype(cm.dtype, np.float64) else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()

    fig.savefig(plotFile, dpi=200, bbox_inches='tight')
    print('Confusion matrix plot file:', plotFile)


def main(tsFile, annoFile, activityModel, normalize, plotFile):
    tsData = pd.read_csv(args.tsFile)
    date_parser = lambda ts: pd.to_datetime([s[:-4] for s in ts])
    annoData = pd.read_csv(args.annoFile, parse_dates=['startTime', 'endTime'],
        date_parser=date_parser)

    if activityModel.endswith("doherty2018.tar"):
        labelColors = DOHERTY_NatComms_COLOURS
        labelDict = buildLabelDict(LABEL_DICTIONARY, DOHERTY_NatComms_DICT_COL)
        labels = DOHERTY_NatComms_LABELS
    elif activityModel.endswith("willetts2018.tar"):
        labelColors = WILLETS_SciReports_COLOURS
        labelDict = buildLabelDict(LABEL_DICTIONARY, WILLETS_SciReports_DICT_COL)
        labels = WILLETS_SciReports_LABELS

    fixTsData(tsData)
    annotateTsData(tsData, annoData, labelDict)
    gatherPredictionLabels(tsData, labels)
    # smooth acceleration
    tsData['acceleration'] = tsData['acceleration'].rolling(window=12, min_periods=1).mean()
    # drop dates without any annotation
    annotatedDates = np.unique(tsData.index.date[tsData['annotation'] != 'undefined'])
    tsData = tsData.loc[np.isin(tsData.index.date, annotatedDates)]

    plotTimeSeries(tsData, labels, labelColors, '{}_timeseries.png'.format(plotFile))

    # compute & plot confusion matrix
    cm, cmLabels = confusionMatrix(tsData, labels, normalize)
    cmFile = '{}_confusion.npz'.format(args.plotFile)
    np.savez(cmFile, cm=cm, cmLabels=cmLabels)
    print('Confusion matrix .npz file: {}'.format(cmFile))
    plotConfusionMatrix(cm, cmLabels, None, '{}_confusion.png'.format(plotFile))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tsFile', help='time series file with predictions by the model')
    parser.add_argument('annoFile', help='camera annotation file')
    parser.add_argument('--activityModel', default='doherty2018.tar')
    parser.add_argument('--normalize', action='store_true')
    parser.add_argument('--plotFile', default='image.png')
    args = parser.parse_args()

    args.plotFile = args.plotFile.split('.')[0]  # remove any extension
    main(args.tsFile, args.annoFile, args.activityModel, args.normalize, args.plotFile)
