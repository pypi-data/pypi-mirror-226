import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import numpy as np
import pandas as pd
import time

import scanpy as sc
from anndata import AnnData
import scanpy.external as sce
from sklearn import metrics

from Utils import *
from sklearn.cluster import KMeans



# get the test model
def buildTestModel(numInputCols,numOutputsCellType,numOutputsRorNR):
    inputLayer = keras.Input(shape=(numInputCols,),name="inputLayer");
    #,kernel_regularizer=calculate_l21_norm
    hiddenLayer1 = keras.layers.Dense(numInputCols+1024, activation='relu',name="hiddenLayer1")(inputLayer);
    hiddenLayer2 = keras.layers.Dense(numInputCols+512, activation='relu',name="hiddenLayer2")(hiddenLayer1);
    hiddenLayer3 = keras.layers.Dense(numInputCols, activation='relu',name="hiddenLayer3")(hiddenLayer2);
    
    cellTypeOutputLayer = keras.layers.Dense(numOutputsCellType, activation='softmax',name="cellTypeOutputLayer")(hiddenLayer3);
    RorNONROutputLayer = keras.layers.Dense(numOutputsRorNR, activation='sigmoid',name="RorNONROutputLayer")(hiddenLayer3);
    
    #Construct the model
    model = keras.Model(inputs=inputLayer,outputs=[cellTypeOutputLayer,RorNONROutputLayer],name="CellTypeDNN");
    return model;


# get the model
def buildModelOld(numInputCols,numOutputsCellType,numOutputsRorNR):
    
    #Impose l2 regularization on the input layer??? Dropout between hidden layers or on the input layer too???
    inputLayer = keras.Input(shape=(numInputCols,),name="inputLayer");
    
    #Hidden layers More nuerons, better result!!!
    dropoutBTWIH1 = keras.layers.Dropout(0.15)(inputLayer); 
    hiddenLayer1 = keras.layers.Dense(40960, activation='relu', kernel_initializer='glorot_normal'
                         ,name="hiddenLayer1")(dropoutBTWIH1);#,kernel_constraint=maxnorm(3)
    #dropoutBTWH1H2 = Dropout(0.2)(hiddenLayer1);
    hiddenLayer2 = keras.layers.Dense(20480, activation='relu', kernel_initializer='glorot_normal'
                         ,name="hiddenLayer2")(hiddenLayer1);#,kernel_constraint=maxnorm(3)
    #dropoutBTWH2H3 = Dropout(0.2)(hiddenLayer2);
    hiddenLayer3 = keras.layers.Dense(10240, activation='relu', kernel_initializer='glorot_normal'
                         ,name="hiddenLayer3")(hiddenLayer2);#,kernel_constraint=maxnorm(3)
    
    hiddenLayer4 = keras.layers.Dense(10240, activation='relu', kernel_initializer='glorot_normal'
                         ,name="hiddenLayer4")(hiddenLayer3);
    hiddenLayer5 = keras.layers.Dense(numInputCols, activation='relu', kernel_initializer='glorot_normal'
                         ,name="hiddenLayer5")(hiddenLayer4);
    
    cellTypeOutputLayer = keras.layers.Dense(numOutputsCellType, activation='softmax',name="cellTypeOutputLayer")(hiddenLayer5);
    
    RorNONROutputLayer = keras.layers.Dense(numOutputsRorNR, activation='sigmoid',name="RorNONROutputLayer")(hiddenLayer5);
    
    #Construct the model
    model = keras.Model(inputs=inputLayer,outputs=[cellTypeOutputLayer,RorNONROutputLayer],name="CellTypeDNN");
    return model;



# get the model
def buildModel(numInputCols,numOutputsCellType,numOutputsRorNR):
    
    '''
    Model for Feldman's data
    
    #Impose l2 regularization on the input layer??? Dropout between hidden layers or on the input layer too???
    inputLayer = keras.Input(shape=(numInputCols,),name="inputLayer");
    
    #Hidden layers More nuerons, better result!!!
    dropoutBTWIH1 = keras.layers.Dropout(0.05)(inputLayer); 
    hiddenLayer1 = keras.layers.Dense(numInputCols+1024, activation='relu', kernel_initializer='glorot_normal'
                         ,name="hiddenLayer1")(dropoutBTWIH1);#,kernel_constraint=maxnorm(3)
    hiddenLayer2 = keras.layers.Dense(numInputCols+512, activation='relu', kernel_initializer='glorot_normal'
                         ,name="hiddenLayer2")(hiddenLayer1);#,kernel_constraint=maxnorm(3)
    #hiddenLayer3 = keras.layers.Dense(numInputCols+512, activation='relu', kernel_initializer='glorot_normal'
    #                     ,name="hiddenLayer3")(hiddenLayer2);#,kernel_constraint=maxnorm(3)
    
    #hiddenLayer4 = keras.layers.Dense(1280, activation='relu', kernel_initializer='glorot_normal'
    #                     ,name="hiddenLayer4")(hiddenLayer3);
    hiddenLayer3 = keras.layers.Dense(numInputCols, activation='relu', kernel_initializer='glorot_normal'
                         ,name="hiddenLayer3")(hiddenLayer2);
    
    cellTypeOutputLayer = keras.layers.Dense(numOutputsCellType, activation='softmax',name="cellTypeOutputLayer")(hiddenLayer3);
    
    RorNONROutputLayer = keras.layers.Dense(numOutputsRorNR, activation='sigmoid',name="RorNONROutputLayer")(hiddenLayer3);
    
    #Construct the model
    model = keras.Model(inputs=inputLayer,outputs=[cellTypeOutputLayer,RorNONROutputLayer],name="CellTypeDNN");
    '''
    
    
    '''
    Model for simulation data
    '''
    inputLayer = keras.Input(shape=(numInputCols,),name="inputLayer");
    dropoutBTWIH1 = keras.layers.Dropout(0.05)(inputLayer); 
    hiddenLayer1 = keras.layers.Dense(numInputCols+1024, activation='relu', kernel_initializer='glorot_normal'
                                      ,name="hiddenLayer1")(dropoutBTWIH1);
    hiddenLayer2 = keras.layers.Dense(numInputCols+512, activation='relu', kernel_initializer='glorot_normal'
                                      ,name="hiddenLayer2")(hiddenLayer1);
    hiddenLayer3 = keras.layers.Dense(numInputCols, activation='relu', kernel_initializer='glorot_normal'
                                      ,name="hiddenLayer3")(hiddenLayer2);
    # hiddenLayer4 = keras.layers.Dense(numInputCols, activation='relu', kernel_initializer='glorot_normal'
    #                                  ,name="hiddenLayer4")(hiddenLayer3);
    # hiddenLayer5 = keras.layers.Dense(numInputCols+512, activation='relu', kernel_initializer='glorot_normal'
    #                                   ,name="hiddenLayer5")(hiddenLayer4);
#     hiddenLayer6 = keras.layers.Dense(numInputCols, activation='relu', kernel_initializer='glorot_normal'
#                                       ,name="hiddenLayer6")(hiddenLayer5);
    #Two branches
    cellTypeOutputLayer = keras.layers.Dense(numOutputsCellType, activation='softmax',name="cellTypeOutputLayer")(hiddenLayer3);
    RorNONROutputLayer = keras.layers.Dense(numOutputsRorNR, activation='sigmoid',name="RorNONROutputLayer")(hiddenLayer3);
    #Construct the model
    model = keras.Model(inputs=inputLayer,outputs=[cellTypeOutputLayer,RorNONROutputLayer],name="CellTypeDNN");
    return model;

#@tf.function
def crossentropyLoss(yTrueLabels,predications,lossFunction,lossWeight):
    crossEntropy = lossFunction(yTrueLabels,predications);
    loss = crossEntropy*lossWeight;
    #print(loss);
    return loss;


#@tf.function
def trainPhase1Model(celltypeModel,trainDataset,epochs,batchSize, celltypeLossWeight, RorNRLossWeight):
    
    # Prepare the training dataset.
    trainDataset = trainDataset.shuffle(buffer_size=1024).batch(batchSize);
    
     # Instantiate an optimizer to train the model.
    optimizer = keras.optimizers.Adam();#learning_rate=0.01
    # Instantiate a loss function for multi-classification.
    categoricalLossFunction = keras.losses.CategoricalCrossentropy();
    # Instantiate a loss function for binary-classification.
    binaryLossFunction = keras.losses.BinaryCrossentropy();
    
    # Prepare the metrics for multi-classification.
    celltypeTrainAccMetric = keras.metrics.CategoricalAccuracy();
    # Prepare the metrics for binary-classification.
    RorNRTrainAccMetric = keras.metrics.BinaryAccuracy();
    
    #Mean loss calculation for multi-classification
    celltypeLossMean = tf.keras.metrics.Mean(name='celltypeLossMean');
    #Mean loss calculation for binary-classification
    RorNRLossMean = tf.keras.metrics.Mean(name='RorNRLossMean');
    
    #lossEpochTable = {};
    
    #Start training the model by 'epochs'.
    for epoch in range(epochs):
        print("\nStart of epoch %d/%d" % (epoch+1,epochs));
        start_time = time.time();
        # Iterate over the batches of the dataset.
        for step, (XTrain, celltypeY,RorNRY) in enumerate(trainDataset):
            # Open a GradientTape to record the operations run
            # during the forward pass, which enables auto-differentiation.
            with tf.GradientTape() as tape:
                # Run the forward pass of the layer. # The operations that the layer applies 
                # to its inputs are going to be recorded # on the GradientTape.
                celltypeOutput,RorNROutput = celltypeModel(XTrain, training=True);
                # Compute the loss value for this minibatch.
                celltypeLossVal = crossentropyLoss(celltypeY,celltypeOutput,categoricalLossFunction,celltypeLossWeight);
                RorNRLossVal = crossentropyLoss(RorNRY,RorNROutput,binaryLossFunction,RorNRLossWeight);
                
                
            # Use the gradient tape to automatically retrieve
            # the gradients of the trainable variables with respect to the loss.
            grads = tape.gradient([celltypeLossVal,RorNRLossVal], celltypeModel.trainable_weights);
            # Run one step of gradient descent by updating
            # the value of the variables to minimize the loss.
            optimizer.apply_gradients(zip(grads, celltypeModel.trainable_weights));

            # Update training metric.
            celltypeTrainAccMetric.update_state(celltypeY, celltypeOutput);
            RorNRTrainAccMetric.update_state(RorNRY, RorNROutput);
            
            #Update mean loss.
            celltypeLossMean.update_state(celltypeLossVal);
            RorNRLossMean.update_state(RorNRLossVal);

        # Display metrics at the end of each epoch.
        celltypeTrainAcc = celltypeTrainAccMetric.result().numpy();
        RorNRTrainAcc = RorNRTrainAccMetric.result().numpy();

        print("Training accuracy for %s: %.4f, accuracy for %s: %.4f." % ("Celltype",float(celltypeTrainAcc),"RorNR",float(RorNRTrainAcc)));
        
        #lossEpochTable[epoch+1] = {"Celltype":1-float(celltypeTrainAcc),"RorNR":1-float(RorNRTrainAcc)};
        
        # Reset training metrics at the end of each epoch
        celltypeTrainAccMetric.reset_states();
        RorNRTrainAccMetric.reset_states();
        
        celltypeLossMean.reset_states();
        RorNRLossMean.reset_states();
        
    return celltypeModel;#,lossEpochTable;

def estimateStandardErrorRange(XTensor,celltypeYTensor,RorNRYTensor,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR,KFoldIterIndices):
    
    curFoldNum = 0;
    celltypeAverageErrorList = [];
    RorNRAverageErrorList = [];
    #Cross validation procedure.
    for trainIdices, testIndices in KFoldIterIndices:
        #Convert indices into tensor object.
        trainIdicesTensor = tf.constant(trainIdices);
        testIndicesTensor = tf.constant(trainIdices);
        #Get training data.
        trainXData = tf.gather(XTensor, trainIdicesTensor);
        trainCellTypeYData = tf.gather(celltypeYTensor, trainIdicesTensor);
        trainRnNRYData = tf.gather(RorNRYTensor, trainIdicesTensor);
        #Get testing data
        testXData = tf.gather(XTensor, testIndicesTensor);
        testCellTypeYData = tf.gather(celltypeYTensor, testIndicesTensor);
        testRnNRYData = tf.gather(RorNRYTensor, testIndicesTensor);
        
        print('KFold validation number {} out of {}'.format(curFoldNum, Configurations.numOfKFolds));
        print('Train data shape: ', trainXData.shape,trainCellTypeYData.shape,trainRnNRYData.shape);
        print('Test data shape: ', testXData.shape, testCellTypeYData.shape,testRnNRYData.shape);
        curFoldNum += 1
        
        #Marge X, multi-class Y, and binary Y into one data object used by Keras network.
        trainDataset = tf.data.Dataset.from_tensor_slices((trainXData, trainCellTypeYData,trainRnNRYData));
        #Construct a model.
        celltypeModel = buildModel(numInputCols,numOutputsCellType,numOutputsRorNR);
        #Train the model.
        celltypeModel = trainPhase1Model(celltypeModel,trainDataset,Configurations.numOfEpochs,Configurations.batchSize,Configurations.celltypeLossWeight, Configurations.RorNRLossWeight);
        
        #Predict
        cellTypeOuput, RnNROutput = celltypeModel.predict(testXData);
        
        #accuracy_score can not process multi-class or multi-label array as prediction, need to convert prediction to 1D.
        cellTypePred=np.argmax(cellTypeOuput, axis=1);
        RnNRPred=np.argmax(RnNROutput, axis=1);
        
        testCellTypeYTrue=np.argmax(testCellTypeYData, axis=1);
        testRnNRYTrue=np.argmax(testRnNRYData, axis=1);
        
        celltypeErrorList = [];
        RorNRErrorList = [];
        for i in range(0,testCellTypeYData.shape[0]):
            
            celltypeError = 0 if testCellTypeYTrue[i] == cellTypePred[i] else 1;
            celltypeErrorList.append(celltypeError);
            
            RorNRError = 0 if testRnNRYTrue[i] == RnNRPred[i] else 1;
            RorNRErrorList.append(RorNRError);
            
        #Calculate the average error and standard error
        celltypeSE = np.std(celltypeErrorList) / np.sqrt(len(celltypeErrorList));
        RorNRSE = np.std(RorNRErrorList) / np.sqrt(len(RorNRErrorList));
     
        celltypeAverageError = np.mean(celltypeErrorList);
        RorNRAverageError = np.mean(RorNRErrorList);
        
        print("celltypeSE: {}, celltypeAverageError: {}, RorNRSE: {}, RorNRAverageError: {}".format(celltypeSE,celltypeAverageError,RorNRSE,RorNRAverageError));
        celltypeAverageErrorList.append(celltypeAverageError);
        RorNRAverageErrorList.append(RorNRAverageError);
        
    #TODO TODO TODO Find the best average error and standard error
    #Calculate the average error and standard error
    celltypeSE = np.std(celltypeAverageErrorList) / np.sqrt(len(celltypeAverageErrorList));
    RorNRSE = np.std(RorNRAverageErrorList) / np.sqrt(len(RorNRAverageErrorList));
    celltypeAverageError = np.mean(celltypeAverageErrorList);
    RorNRAverageError = np.mean(RorNRAverageErrorList);
    print("Average celltypeSE: {}, Average celltypeAverageError: {}, Average RorNRSE: {}, Average RorNRAverageError: {}".format(celltypeSE,celltypeAverageError,RorNRSE,RorNRAverageError));
    return celltypeSE,celltypeAverageError,RorNRSE,RorNRAverageError;
    

#@tf.function
def phase2CrossentropyLoss(yTrueLabels,predications,lossFunction,lossWeight,alpha,clusteringLoss):
    '''''' '''''' '''''' '''''' ''''''
    #Add the clustering loss to both losses???
    '''''' '''''' '''''' '''''' ''''''
    crossEntropy = lossFunction(yTrueLabels,predications);
    loss = lossWeight*crossEntropy+alpha*clusteringLoss+lossWeight;
    #print(loss);
    return loss;


#@tf.function
def trainPhase2Model(celltypeModel,trainDataset,epochs,batchSize, celltypeLossWeight, RorNRLossWeight,alpha,curK):
    # Prepare the training dataset.
    trainDataset = trainDataset.shuffle(buffer_size=1024).batch(batchSize);
    
     # Instantiate an optimizer to train the model.
    optimizer = keras.optimizers.Adam();#learning_rate=0.01
    # Instantiate a loss function for multi-classification.
    categoricalLossFunction = keras.losses.CategoricalCrossentropy();
    # Instantiate a loss function for binary-classification.
    binaryLossFunction = keras.losses.BinaryCrossentropy();
    
    # Prepare the metrics for multi-classification.
    celltypeTrainAccMetric = keras.metrics.CategoricalAccuracy();
    # Prepare the metrics for binary-classification.
    RorNRTrainAccMetric = keras.metrics.BinaryAccuracy();
    
    #Mean loss calculation for multi-classification
    celltypeLossMean = tf.keras.metrics.Mean(name='celltypeLossMean');
    #Mean loss calculation for binary-classification
    RorNRLossMean = tf.keras.metrics.Mean(name='RorNRLossMean');
    
    clusteringLoss = 0;
    
    #Start training the model by 'epochs'.
    for epoch in range(epochs):
        print("\nStart of epoch %d/%d" % (epoch+1,epochs));
        start_time = time.time();
        # Iterate over the batches of the dataset.
        for step, (XTrain, celltypeY,RorNRY) in enumerate(trainDataset):
            # Open a GradientTape to record the operations run
            # during the forward pass, which enables auto-differentiation.
            with tf.GradientTape() as tape:
                # Run the forward pass of the layer. # The operations that the layer applies 
                # to its inputs are going to be recorded # on the GradientTape.
                celltypeOutput,RorNROutput = celltypeModel(XTrain, training=True);
                # Compute the loss value for this minibatch.
                celltypeLossVal = phase2CrossentropyLoss(celltypeY,celltypeOutput,categoricalLossFunction,celltypeLossWeight,alpha,clusteringLoss);
                RorNRLossVal = phase2CrossentropyLoss(RorNRY,RorNROutput,binaryLossFunction,RorNRLossWeight,alpha,clusteringLoss);
                
                
            # Use the gradient tape to automatically retrieve
            # the gradients of the trainable variables with respect to the loss.
            grads = tape.gradient([celltypeLossVal,RorNRLossVal], celltypeModel.trainable_weights);
            # Run one step of gradient descent by updating
            # the value of the variables to minimize the loss.
            optimizer.apply_gradients(zip(grads, celltypeModel.trainable_weights));

            # Update training metric.
            celltypeTrainAccMetric.update_state(celltypeY, celltypeOutput);
            RorNRTrainAccMetric.update_state(RorNRY, RorNROutput);
            
            #Update mean loss.
            celltypeLossMean.update_state(celltypeLossVal);
            RorNRLossMean.update_state(RorNRLossVal);
            

        # Display metrics at the end of each epoch.
        celltypeTrainAcc = celltypeTrainAccMetric.result().numpy();
        RorNRTrainAcc = RorNRTrainAccMetric.result().numpy();

        print("Training accuracy for %s: %.4f, accuracy for %s: %.4f." % ("Celltype",float(celltypeTrainAcc),"RorNR",float(RorNRTrainAcc)));
        
        # Reset training metrics at the end of each epoch
        celltypeTrainAccMetric.reset_states();
        RorNRTrainAccMetric.reset_states();
        
        celltypeLossMean.reset_states();
        RorNRLossMean.reset_states();
        
        #Calculate clustering loss
        #Get representation data
        representationLayerModel = tf.keras.models.Model(inputs=celltypeModel.input,outputs=celltypeModel.get_layer("hiddenLayer3").output);
        representationLayterOutput = representationLayerModel.predict(trainDataset);
        kmeans = KMeans(n_clusters=curK, random_state=0).fit(representationLayterOutput);
        clusteringLoss = kmeans.inertia_*alpha;
        print("representationLayterOutput.shape: "+str(representationLayterOutput.shape));
        print("alpha: "+str(alpha));
        print("clusteringLoss: "+str(clusteringLoss));
        print("celltypeLossVal: "+str(celltypeLossVal));
        print("RorNRLossVal: "+str(RorNRLossVal));
        
    return celltypeModel;

def phase2CrossValidation(curK,alpha,XTensor,celltypeYTensor,RorNRYTensor,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR,KFoldIterIndices):
    
    curFoldNum = 0;
    meanSilhouetteScoreList = [];
    meanCelltypeErrorList = [];
    meanRorNRErrorList = [];
    #Cross validation procedure.
    for trainIdices, testIndices in KFoldIterIndices:
        #Convert indices into tensor object.
        trainIdicesTensor = tf.constant(trainIdices);
        testIndicesTensor = tf.constant(trainIdices);
        #Get training data.
        trainXData = tf.gather(XTensor, trainIdicesTensor);
        trainCellTypeYData = tf.gather(celltypeYTensor, trainIdicesTensor);
        trainRnNRYData = tf.gather(RorNRYTensor, trainIdicesTensor);
        #Get testing data
        testXData = tf.gather(XTensor, testIndicesTensor);
        testCellTypeYData = tf.gather(celltypeYTensor, testIndicesTensor);
        testRnNRYData = tf.gather(RorNRYTensor, testIndicesTensor);
        
        print('KFold validation number {} out of {}'.format(curFoldNum, Configurations.numOfKFolds));
        print('Train data shape: ', trainXData.shape,trainCellTypeYData.shape,trainRnNRYData.shape);
        print('Test data shape: ', testXData.shape, testCellTypeYData.shape,testRnNRYData.shape);
        curFoldNum += 1
        
        #Marge X, multi-class Y, and binary Y into one data object used by Keras network.
        trainDataset = tf.data.Dataset.from_tensor_slices((trainXData, trainCellTypeYData,trainRnNRYData));
        #Construct a model.
        celltypeModel = buildModel(numInputCols,numOutputsCellType,numOutputsRorNR);
        #Train the model.
        celltypeModel = trainPhase2Model(celltypeModel,trainDataset,Configurations.numOfEpochs,Configurations.batchSize,Configurations.celltypeLossWeight, Configurations.RorNRLossWeight,alpha,curK);
        
        #Predict
        cellTypeOuput, RnNROutput = celltypeModel.predict(testXData);
        
        #accuracy_score can not process multi-class or multi-label array as prediction, need to convert prediction to 1D.
        cellTypePred=np.argmax(cellTypeOuput, axis=1);
        RnNRPred=np.argmax(RnNROutput, axis=1);
        
        testCellTypeYTrue=np.argmax(testCellTypeYData, axis=1);
        testRnNRYTrue=np.argmax(testRnNRYData, axis=1);
        
        celltypeErrorList = [];
        RorNRErrorList = [];
        for i in range(0,testCellTypeYData.shape[0]):
            
            celltypeError = 0 if testCellTypeYTrue[i] == cellTypePred[i] else 1;
            celltypeErrorList.append(celltypeError);
            
            RorNRError = 0 if testRnNRYTrue[i] == RnNRPred[i] else 1;
            RorNRErrorList.append(RorNRError);
            
        #Calculate the average error and standard error
        curCelltypeSE = np.std(celltypeErrorList) / np.sqrt(len(celltypeErrorList));
        curRorNRSE = np.std(RorNRErrorList) / np.sqrt(len(RorNRErrorList));
        curCelltypeAverageError = np.mean(celltypeErrorList);
        curRorNRAverageError = np.mean(RorNRErrorList);
        
        print("curCelltypeSE: {}, curCelltypeAverageError: {}, curRorNRSE: {}, curRorNRAverageError: {}".format(curCelltypeSE,curCelltypeAverageError,curRorNRSE,curRorNRAverageError));
        
        #Test clustering
        representationLayerModel = keras.Model(inputs=celltypeModel.input,outputs=celltypeModel.get_layer("hiddenLayer2").output)
        representationLayterOutput = representationLayerModel.predict(trainXData);
        
        '''
        dframe = pd.DataFrame(representationLayterOutput);
        dframe.index, dframe.columns = (map(str, dframe.index), map(str, dframe.columns));
        adata = AnnData(dframe);
        res = sc.tl.pca(adata, n_comps=curK);
        #communities,graph, modularityScore =  ,copy=True
        communities,graph, modularityScore = sce.tl.phenograph(adata, clustering_algo="louvain", k=curK,copy=True);
        silhouetteScore = metrics.silhouette_score(representationLayterOutput, communities);
        '''
        kmeans = KMeans(n_clusters=curK, random_state=0).fit(representationLayterOutput);
        silhouetteScore = metrics.silhouette_score(representationLayterOutput, kmeans.labels_);
        print("silhouetteScore: {}".format(silhouetteScore));
        
        meanSilhouetteScoreList.append(silhouetteScore);
        meanCelltypeErrorList.append(curRorNRAverageError);
        meanRorNRErrorList.append(curRorNRAverageError);
        
    return np.mean(meanSilhouetteScoreList),np.mean(meanCelltypeErrorList),np.mean(meanRorNRErrorList);
def findOptimalHyperparameters(initialK,KThreshold,alphaList,celltypeSE,celltypeAverageError,RorNRSE,RorNRAverageError,dataset,cellTypeData,RorNRData):
    selectedK = initialK;
    '''''' '''''' '''''' '''''' ''''''
    #Alpha should be based on the number of samples.
    #Because the more sample, the bigger the clustering loss is. And the clustering loss is a huge number, i.e, 169877766.
    #Therefore, alpha should be a small number, at a point where it should be at the same scale as other losses.
    #So pick alpha values carefully.
    '''''' '''''' '''''' '''''' ''''''
    selectedAlpha = alphaList[0];
    selectedSilhouetteScore = -1;
    randomStateCounter = 1;
    for i in range(KThreshold):
        curK = initialK+i+1;
        tempSilhouetteScore = -1;
        #Get the alpha with the largest silhouette score 
        for j in range(len(alphaList)):
            alpha = alphaList[j];
            print("Alpha: {}".format(alpha));
            
            #Load the raw data for cross-validation
            randomStateCounter=randomStateCounter+1;
            XTensor,celltypeYTensor,RorNRYTensor,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR,KFoldIterIndices = splitDataForCV(dataset,cellTypeData,RorNRData,randomStateCounter);
    
            meanSilhouetteScore,meanCelltypeError,meanRorNRError= phase2CrossValidation(curK,alpha,XTensor,celltypeYTensor,RorNRYTensor,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR,KFoldIterIndices);
            #Perform one standard error rule
            if (meanCelltypeError <= (celltypeSE+celltypeAverageError)) and (meanRorNRError <= (RorNRSE+RorNRAverageError)):
                tempSilhouetteScore = meanSilhouetteScore;
        if selectedSilhouetteScore<=tempSilhouetteScore:
            selectedSilhouetteScore = tempSilhouetteScore;
            selectedK = curK;
            selectedAlpha = alpha;
    return selectedK,selectedAlpha;


def main():
    
    cellTypeNumericMap = {'B1':1,'B2':2,'B3':3,'B4':4,'B5':5,'B6':6};
    RorNRNumericMap = {'A':1,'B':0};
    dirPath = "SimulationData/";
    expressionMatrixPath = dirPath+"SimulationLogCounts.csv";
    cellTypeDataPath = dirPath+"CellTypeDF.csv";
    RorNRDataPath = dirPath+"RorNRDF.csv";
    XTensor,celltypeYTensor,RorNRYTensor,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR,KFoldIterIndices = loadRawSimulationDataForCV(1,expressionMatrixPath,cellTypeDataPath,RorNRDataPath,cellTypeNumericMap,RorNRNumericMap);
    #dataset,cellTypeData,RorNRData = loadRawData2();
    '''
    #Load the raw data for cross-validation
    XTensor,celltypeYTensor,RorNRYTensor,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR,KFoldIterIndices = splitDataForCV(dataset,cellTypeData,RorNRData,50);
    '''
    celltypeSE,celltypeAverageError,RorNRSE,RorNRAverageError = estimateStandardErrorRange(XTensor,celltypeYTensor,RorNRYTensor,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR,KFoldIterIndices);
    
    
    
    '''
    celltypeSE =  0.0010104162;
    celltypeAverageError = 0.0047174545;
    RorNRSE = 0.0052783214;
    RorNRAverageError = 0.0219712937;
    
    alphaList = [0.000000005];
    initialK = 11;
    KThreshold = 6;
    selectedK,selectedAlpha = findOptimalHyperparameters(initialK,KThreshold,alphaList,celltypeSE,celltypeAverageError,RorNRSE,RorNRAverageError,dataset,cellTypeData,RorNRData);
    print("The best K: {}".format(selectedK));
    
    # Opening a file
    file = open('FineResult1.txt', 'w');
    strLine = "The best K: "+str(selectedK)+", the best alpha: "+str(selectedAlpha)+"\n";
    file.write(strLine);
    file.close();
    '''
    
    
if __name__ == "__main__":
    main();
    
#     X, Y, celltypeY, RnNRY = loadData();
#     print(X.shape);
#     print(celltypeY.shape);
#     print(RnNRY.shape);
#     Configurations.numOfInputRows = X.shape[0];
#     Configurations.numOfInputCols = X.shape[1];
#     Configurations.numOfCellTypeOuputClasses = celltypeY.shape[1];
#     Configurations.numOfRorNROuputClasses = RnNRY.shape[1];
#     Configurations.NumOfNeuronsInHiddenLayer4 = 10240;
#     Configurations.NumOfNeuronsInHiddenLayer3 = Configurations.NumOfNeuronsInHiddenLayer4*2;
#     Configurations.NumOfNeuronsInHiddenLayer2 = Configurations.NumOfNeuronsInHiddenLayer3*2;
#     Configurations.NumOfNeuronsInHiddenLayer1 = Configurations.NumOfNeuronsInHiddenLayer2*2;
#     crossValidation(X, Y, celltypeY, RnNRY);
    
    '''
    dirPath = "Feldman/";
    fileName = "GSE120575_Sade_Feldman_melanoma_single_cells_TPM_GEO.txt";
    trainDataset,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR = loadRawData(dirPath,fileName);
    #trainDataset,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR = loadClassificationData(1500, 10, 5, 6);
    print("# of rows in X: {}, # of cols in : {}, # of cols in celltyple: {}, and # of rows in RorNR: {}".format(numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR));
    
    celltypeModel = buildModel(numInputCols,numOutputsCellType,numOutputsRorNR);
    epochs = 20;
    batchSize = 64;
    celltypeLossWeight, RorNRLossWeight = 0.9,0.1;
    trainPhase1Model(celltypeModel,trainDataset,epochs,batchSize,celltypeLossWeight, RorNRLossWeight);
    '''
    
    
    #Load simulation data for cross-validation
    #XTensor,celltypeYTensor,RorNRYTensor,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR,KFoldIterIndices = loadClassificationDataForCV(3000, 10, 5, 6);