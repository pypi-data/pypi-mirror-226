
numOfInputRows = 0;
numOfInputCols = 0;
numOfCellTypeOuputClasses = 0;
numOfRorNROuputClasses = 0;

NumOfNeuronsInHiddenLayer1 = 0;
NumOfNeuronsInHiddenLayer2 = 0;
NumOfNeuronsInHiddenLayer3 = 0;
NumOfNeuronsInHiddenLayer4 = 0;


numOfKFolds = 10;
numOfEpochs = 60;
batchSize = 32;

#The final prediction accurracy is high, meaning that all the weights will converge, 
#meanning they will end up with similar from a run to another.
#Therefore, I doubt different weights on these two output could have an obvious difference.
celltypeLossWeight = 1;
RorNRLossWeight = 1;

celltypeColorMap = {1:'grey', 2:'purple', 3:'blue', 4:'black', 5:'orange', 6:'red', 7:'olive'
                    , 8:'pink', 9:'brown', 10:'cyan', 11:'lime'};

    
'''
def setConfigurations():
    numOfInputRows = 0;
    numOfInputCols = 0;
    numOfCellTypeOuputClasses 0;
    numOfRorNROuputClasses = 0;
'''