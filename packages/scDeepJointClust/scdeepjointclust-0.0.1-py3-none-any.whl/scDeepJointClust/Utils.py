import numpy as np
import pandas as pd
import gc

from sklearn.datasets import make_regression
from sklearn.datasets import make_multilabel_classification
from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold

import tensorflow as tf

import Configurations as Configurations

import matplotlib.pyplot as plt
from matplotlib import ticker
import matplotlib.lines as mlines
from sklearn import manifold
from sklearn.decomposition import PCA,TruncatedSVD

# Generate a regression model dataset.
def generateRegressionDataset():
    X, Y = make_regression(n_samples=1000, n_features=7, n_informative=3, n_targets=2, random_state=2);
    return X, Y;

# Generate a classification model dataset
def generateClassificationDataset(numSamples, numFeatures, numInformative, numClasses):
    X, Y = make_classification(n_samples=numSamples, n_features=numFeatures, n_informative=numInformative
                               , n_classes=numClasses, random_state=1,n_clusters_per_class=2);
    return X,Y;
    
#Generate a multilabel classification model dataset.
def generateMultiLabelsClassificationDataset(numSamples,numFeatures,numClasses,numLabels):
    X, Y, p_c, p_w_c = make_multilabel_classification(n_samples=numSamples, n_features=numFeatures,n_classes=numClasses
                                                      , n_labels=numLabels, random_state=2, return_distributions=True
                                                      ,return_indicator=False)
    return X,Y, p_c, p_w_c;

def loadClassificationData(numSamples, numFeatures, numInformative, numClasses):
    #Simulate classification data.
    X, Y = make_classification(n_samples=numSamples, n_features=numFeatures, n_informative=numInformative, n_classes=numClasses, random_state=1);
    
    #Convert X into a tensor object.
    XTensor = tf.convert_to_tensor(X);
    #Convert Y into one hot vector format and and then a tensor object.
    celltypeYTensor = tf.keras.utils.to_categorical(Y);
    celltypeYTensor = tf.convert_to_tensor(celltypeYTensor);
    #Make binary data from the multi-class Y data.
    #Then, convert the binary data into one hot vector and a tensor object.
    Y = Y < 3;
    Y = Y.astype(int);
    RorNRYTensor = tf.keras.utils.to_categorical(Y);
    RorNRYTensor = tf.convert_to_tensor(RorNRYTensor);
    
    #Marge X, multi-class Y, and binary Y into one data object used by Keras network.
    trainDataset = tf.data.Dataset.from_tensor_slices((XTensor, celltypeYTensor,RorNRYTensor));
    
    #Collect data information.
    numInputRows = XTensor.shape[0];
    numInputCols = XTensor.shape[1];
    numOutputsCellType = celltypeYTensor.shape[1];
    numOutputsRorNR = RorNRYTensor.shape[1];
    
    print(XTensor.shape);
    print(celltypeYTensor.shape);
    print(RorNRYTensor.shape);
    
    return trainDataset,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR;

def loadClassificationDataForCV(numSamples, numFeatures, numInformative, numClasses):
    #Simulate classification data.
    X, Y = make_classification(n_samples=numSamples, n_features=numFeatures, n_informative=numInformative, n_classes=numClasses, random_state=1);
    
    #Splitting iterations in the cross-validator.
    kfold = StratifiedKFold(n_splits=Configurations.numOfKFolds, shuffle=True, random_state=51);
    KFoldIterIndices = kfold.split(X,Y);
    
    #Convert X into a tensor object.
    XTensor = tf.convert_to_tensor(X);
    #Convert Y into one hot vector format and and then a tensor object.
    celltypeYTensor = tf.keras.utils.to_categorical(Y);
    celltypeYTensor = tf.convert_to_tensor(celltypeYTensor);
    #Make binary data from the multi-class Y data.
    #Then, convert the binary data into one hot vector and a tensor object.
    Y = Y < 3;
    Y = Y.astype(int);
    RorNRYTensor = tf.keras.utils.to_categorical(Y);
    RorNRYTensor = tf.convert_to_tensor(RorNRYTensor);
    
    
    #Collect data information.
    numInputRows = XTensor.shape[0];
    numInputCols = XTensor.shape[1];
    numOutputsCellType = celltypeYTensor.shape[1];
    numOutputsRorNR = RorNRYTensor.shape[1];
    
    print(XTensor.shape);
    print(celltypeYTensor.shape);
    print(RorNRYTensor.shape);
    
    return XTensor,celltypeYTensor,RorNRYTensor,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR,KFoldIterIndices;



def loadRawData(dirPath,fileName):
    dirPath = "Feldman/";
    dataset = pd.read_csv(dirPath+"GSE120575_Sade_Feldman_melanoma_single_cells_TPM_GEO.txt",header=0, index_col=0);
    
    selectedGenes = pd.read_csv(dirPath+"selected_genes.csv",header=0, index_col=0);
    selectedSamples = pd.read_csv(dirPath+"selected_samples.csv",header=0, index_col=0);
    selectedGeneList = selectedGenes.index.to_list();
    selectedGeneList.append('RorRN');
    selectedGeneList.append('CellType');
    selectedSampleList = selectedSamples.index.to_list();
    print(len(selectedGeneList));
    print(len(selectedSampleList));
    dataset = dataset[selectedGeneList];
    dataset = dataset.loc[selectedSampleList];
    print(dataset.shape);
    
    RorNR = dataset['RorRN'];
    RorNR = RorNR.map({'R':1,'NR':0},na_action=None);
    
    cellType = dataset['CellType'];
    cellType = cellType.astype(int)
    
    colList = dataset.columns.tolist();
    colList.remove("CellType");
    colList.remove("RorRN");
    dataset = dataset[colList];
    
    XTensor = tf.convert_to_tensor(dataset);
    
    celltypeYTensor = tf.keras.utils.to_categorical(cellType-1);
    celltypeYTensor = tf.convert_to_tensor(celltypeYTensor);
    
    RorNRYTensor = tf.keras.utils.to_categorical(RorNR);
    RorNRYTensor = tf.convert_to_tensor(RorNRYTensor);
    
    trainDataset = tf.data.Dataset.from_tensor_slices((XTensor, celltypeYTensor,RorNRYTensor));
    numInputRows = XTensor.shape[0];
    numInputCols = XTensor.shape[1];
    numOutputsCellType = celltypeYTensor.shape[1];
    numOutputsRorNR = RorNRYTensor.shape[1];
    
    print(XTensor.shape);
    print(celltypeYTensor.shape);
    print(RorNRYTensor.shape);
    
    return trainDataset,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR;

def loadRawDataset():
    dirPath = "Feldman/";
    dataset = pd.read_csv(dirPath+"GSE120575_Sade_Feldman_melanoma_single_cells_TPM_GEO.txt",header=0, index_col=0);
    
    selectedGenes = pd.read_csv(dirPath+"selected_genes.csv",header=0, index_col=0);
    selectedSamples = pd.read_csv(dirPath+"selected_samples.csv",header=0, index_col=0);
    selectedGeneList = selectedGenes.index.to_list();
    selectedGeneList.append('RorRN');
    selectedGeneList.append('CellType');
    selectedSampleList = selectedSamples.index.to_list();
    print(len(selectedGeneList));
    print(len(selectedSampleList));
    dataset = dataset[selectedGeneList];
    dataset = dataset.loc[selectedSampleList];
    print(dataset.shape);
    
    RorNR = dataset['RorRN'];
    RorNR = RorNR.map({'R':1,'NR':0},na_action=None);
    
    cellType = dataset['CellType'];
    cellType = cellType.astype(int)
    
    colList = dataset.columns.tolist();
    colList.remove("CellType");
    colList.remove("RorRN");
    dataset = dataset[colList];
    
    return dataset,cellType,RorNR;

def loadRawDataForCV(randomState):
    '''
    dirPath = "Feldman/";
    dataset = pd.read_csv(dirPath+"GSE120575_Sade_Feldman_melanoma_single_cells_TPM_GEO.txt",header=0, index_col=0);
    
    selectedGenes = pd.read_csv(dirPath+"selected_genes.csv",header=0, index_col=0);
    selectedSamples = pd.read_csv(dirPath+"selected_samples.csv",header=0, index_col=0);
    selectedGeneList = selectedGenes.index.to_list();
    selectedGeneList.append('RorRN');
    selectedGeneList.append('CellType');
    selectedSampleList = selectedSamples.index.to_list();
    print(len(selectedGeneList));
    print(len(selectedSampleList));
    dataset = dataset[selectedGeneList];
    dataset = dataset.loc[selectedSampleList];
    print(dataset.shape);
    
    RorNR = dataset['RorRN'];
    RorNR = RorNR.map({'R':1,'NR':0},na_action=None);
    
    cellType = dataset['CellType'];
    cellType = cellType.astype(int)
    
    colList = dataset.columns.tolist();
    colList.remove("CellType");
    colList.remove("RorRN");
    dataset = dataset[colList];
    '''
    dataset,cellTypeData,RorNRData = loadRawDataset();
    
    #Splitting iterations in the cross-validator.
    kfold = StratifiedKFold(n_splits=Configurations.numOfKFolds, shuffle=True, random_state=randomState);
    KFoldIterIndices = kfold.split(dataset,cellTypeData);
    
    XTensor = tf.convert_to_tensor(dataset);
    
    celltypeYTensor = tf.keras.utils.to_categorical(cellTypeData-1);
    celltypeYTensor = tf.convert_to_tensor(celltypeYTensor);
    
    RorNRYTensor = tf.keras.utils.to_categorical(RorNRData);
    RorNRYTensor = tf.convert_to_tensor(RorNRYTensor);
    
    trainDataset = tf.data.Dataset.from_tensor_slices((XTensor, celltypeYTensor,RorNRYTensor));
    numInputRows = XTensor.shape[0];
    numInputCols = XTensor.shape[1];
    numOutputsCellType = celltypeYTensor.shape[1];
    numOutputsRorNR = RorNRYTensor.shape[1];
    
    print(XTensor.shape);
    print(celltypeYTensor.shape);
    print(RorNRYTensor.shape);
    
    return XTensor,celltypeYTensor,RorNRYTensor,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR,KFoldIterIndices;

def loadRawData2():
    dirPath = "Feldman/";
    dataset = pd.read_csv(dirPath+"filteredDataset.csv",index_col=0);
    
    filteredCelltypes = pd.read_csv(dirPath+"filteredCelltypes.csv",index_col=0);
    filteredRorNRFlags = pd.read_csv(dirPath+"filteredRorNRFlag.csv",index_col=0);
    
    
    cellTypeData = filteredCelltypes["Celltype"].values;
    RorNRData = filteredRorNRFlags["RorNR"].values;
    return dataset,cellTypeData,RorNRData;
    
def splitDataForCV(dataset,cellTypeData,RorNRData,randomState):
    
    #Release dataframe memory
#     del [[filteredCelltypes,filteredRorNRFlags]];
#     gc.collect();
#     filteredCelltypes=pd.DataFrame();
#     filteredRorNRFlags=pd.DataFrame();
    
    
    #Splitting iterations in the cross-validator.
    kfold = StratifiedKFold(n_splits=Configurations.numOfKFolds, shuffle=True, random_state=randomState);
    KFoldIterIndices = kfold.split(dataset,cellTypeData);
    
    XTensor = tf.convert_to_tensor(dataset);
    #Release dataframe memory
#     del [[dataset]];
#     gc.collect();
#     dataset=pd.DataFrame();
    
    #The classes starts at 0, so we need to minus 1 to all the class values
    celltypeYTensor = tf.keras.utils.to_categorical(cellTypeData-1);
    celltypeYTensor = tf.convert_to_tensor(celltypeYTensor);

    
    RorNRYTensor = tf.keras.utils.to_categorical(RorNRData);
    RorNRYTensor = tf.convert_to_tensor(RorNRYTensor);


    trainDataset = tf.data.Dataset.from_tensor_slices((XTensor, celltypeYTensor,RorNRYTensor));
    numInputRows = XTensor.shape[0];
    numInputCols = XTensor.shape[1];
    numOutputsCellType = celltypeYTensor.shape[1];
    numOutputsRorNR = RorNRYTensor.shape[1];
    
    return XTensor,celltypeYTensor,RorNRYTensor,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR,KFoldIterIndices;

'''
    The DNN model needs numeric values, therefore, we need to use numeric values to replace string values.
    cellTypeNumericMap: maps string celltype values to numeric values.
    RorNRNumericMap: maps string RorNR values to numeric values.
'''
def loadConditionSimulationData(expressionMatrixPath,cellTypeDataPath,RorNRDataPath,cellTypeNumericMap,RorNRNumericMap):
    dataset = pd.read_csv(expressionMatrixPath,header=0,index_col=0);
    
    cellTypeData = pd.read_csv(cellTypeDataPath,header=0);
    cellTypeData["Celltype"] = cellTypeData["Celltype"].map(cellTypeNumericMap,na_action=None);
    
    RorNRDF = pd.read_csv(RorNRDataPath,header=0);#,index_col=0
    RorNRDF["RorNR"] = RorNRDF["RorNR"].map(RorNRNumericMap,na_action=None);
    return dataset,cellTypeData,RorNRDF;
    #conditionDF.columns = ["Condition"];
    #conditionDF.to_csv(dirPath+"conditionDF.csv",index=None)
    #blockDF.columns = ["Block"];
    #blockDF.to_csv(dirPath+"blockDF.csv",index=None)
    #conditionDF.columns = ["Condition"];
    #conditionDF.to_csv(dirPath+"conditionDF.csv",index=None)
    #print(cellTypeData)

def loadRawSimulationDataForCV(randomState,expressionMatrixPath,cellTypeDataPath,RorNRDataPath,cellTypeNumericMap,RorNRNumericMap):
    
    dataset,cellTypeData,RorNRData = loadConditionSimulationData(expressionMatrixPath,cellTypeDataPath,RorNRDataPath,cellTypeNumericMap,RorNRNumericMap);
    
    #Splitting iterations in the cross-validator. 
    kfold = StratifiedKFold(n_splits=Configurations.numOfKFolds, shuffle=True, random_state=randomState);
    KFoldIterIndices = kfold.split(dataset,cellTypeData);
    
    XTensor = tf.convert_to_tensor(dataset);
    
    celltypeYTensor = tf.keras.utils.to_categorical(cellTypeData-1);
    celltypeYTensor = tf.convert_to_tensor(celltypeYTensor);
    
    RorNRYTensor = tf.keras.utils.to_categorical(RorNRData);
    RorNRYTensor = tf.convert_to_tensor(RorNRYTensor);
    
    trainDataset = tf.data.Dataset.from_tensor_slices((XTensor, celltypeYTensor,RorNRYTensor));
    numInputRows = XTensor.shape[0];
    numInputCols = XTensor.shape[1];
    numOutputsCellType = celltypeYTensor.shape[1];
    numOutputsRorNR = RorNRYTensor.shape[1];
    
    print(XTensor.shape);
    print(celltypeYTensor.shape);
    print(RorNRYTensor.shape);
    
    return XTensor,celltypeYTensor,RorNRYTensor,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR,KFoldIterIndices;

def plotTSNE(dataset,celltypeColorArr,RorNRZeroMask,RorNROneMask,celltypeColorMap,numComponents,pathToSave):
    
    #pcaModel = PCA(n_components=numComponents);#PCA,TruncatedSVD
    #pcaResult = pcaModel.fit_transform(dataset);
    #print(pcaResult.shape)
    TSNEModel = manifold.TSNE(
        n_components=2,# number of coordinates for the manifold
        perplexity=50,
        n_iter=10000,
        init="pca"
    );
    STSNEPoints = TSNEModel.fit_transform(dataset);#pcaResult
    x, y = STSNEPoints.T;

    fig, ax = plt.subplots(figsize=(16, 16), facecolor="white", constrained_layout=True);
    NRScatter = ax.scatter(x[RorNRZeroMask], y[RorNRZeroMask], c=celltypeColorArr[RorNRZeroMask], s=15,marker='x',label="Non-responder");
    RScatter = ax.scatter(x[RorNROneMask], y[RorNROneMask], c=celltypeColorArr[RorNROneMask], s=15,marker='o',label="Responder");
    
    #Create RorNR legend
    
#     NRScatter.set_color('black');
#     RScatter.set_color('black');
    RorNRLegend = plt.legend(handles=[NRScatter, RScatter],loc="upper right", bbox_to_anchor=(0.9, 1), prop={'size': 18});
    RorNRLegend.legendHandles[0].set_color('black');
    RorNRLegend.legendHandles[1].set_color('black');
    
    #Add celltype legend
    handleList = [];
    for key,value in celltypeColorMap.items():
        tHandle = mlines.Line2D([], [], color=value, marker='o', ls='',label=key);
        handleList.append(tHandle);
    plt.legend(handles=handleList,loc="upper right", prop={'size': 18});
    #Add RorNR legend
    plt.gca().add_artist(RorNRLegend);
    
    plt.xlabel("tSNE1", fontsize=18);
    plt.ylabel("tSNE2", fontsize=18);
    plt.xticks(fontsize=18);
    plt.yticks(fontsize=18);

    # #     ax.xaxis.set_major_formatter(ticker.NullFormatter());
    # #     ax.yaxis.set_major_formatter(ticker.NullFormatter());
    plt.savefig(pathToSave,dpi=320);
    plt.show();



def main():
    #Test data simulation
    #X,Y = generateClassificationDataset(1500, 10, 6, 5);
    #X,Y,p_c, p_w_c = generateMultiLabelsClassificationDataset(1500, 10, 2, 3);
    #print(Y.shape);
    #print(X.shape);
    print("Main");
if __name__ == "__main__":
    main();