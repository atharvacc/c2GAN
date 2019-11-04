function folder_split_into_trainA_and_trainB(srcA, srcB, trainA, trainB, testA, testB)
% separate all file in a folder in 2 part,
% one for trainA,
% one for trainB
%
listA = dir(srcA); listA = listA(3:end);
listB = dir(srcB); listB = listB(3:end);

nb = length(listA);

nb_test = floor(nb/10);

nb_train = floor(nb*0.9/2);


for i =1:nb
    
    if mod(i,100)==0
        fprintf('Processing: %d of %d...\n', i, length(listA))
    end
    
    nameA = fullfile(listA(i).folder, listA(i).name);
    imgA = imread(nameA);
    imgA = im2uint8(imgA);
    
    nameB = fullfile(listB(i).folder, listB(i).name);
    imgB = imread(nameB);
    imgB = im2uint8(imgB);
    
    % for test
    if i<=nb_test
        
        imwrite(imgA, fullfile(testA, listA(i).name))
        imwrite(imgB, fullfile(testB, listB(i).name))
        
    end
    
    % 1
    if nb_test<i && i<= floor(nb*0.55)
        
        imwrite(imgA, fullfile(trainA, listA(i).name))
        
    end
    
    % 2
    if i>floor(nb*0.55)
        
        imwrite(imgB, fullfile(trainB, listB(i).name))
        
    end
    
end