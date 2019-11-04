clc;clear;

folderA = './raw/testA/';
folderB = './raw/testB-GT/';

patch_size = 256;
overlap = 32;

%% for A
list = dir([folderA '*.tif']);
for i = 1:length(list)
    
    fprintf('%d of %d...\n', i, length(list))
    imgA = loadtiff(fullfile(list(i).folder, list(i).name));
    [xs, ys, zs] = size(imgA);
    
    % split
    for j = 1:floor(xs/(patch_size-overlap))
        for k = 1:floor(ys/(patch_size-overlap))
            
            xi = 1+(j-1)*(patch_size-overlap);
            yi = 1+(k-1)*(patch_size-overlap);
            
            img = imgA(xi:xi+patch_size-1,yi:yi+patch_size-1,:);
            
            saveastiff(img, ['./testA/file' num2str(i) '_' num2str(xi) '_' num2str(yi) '_' num2str(xs) '_' num2str(ys) '_' num2str(patch_size) '_' num2str(overlap) '_.tif']);
        end
    end
    
end

%% for B
list = dir([folderB '*.png']);
for i = 1:length(list)
    
    fprintf('%d of %d...\n', i, length(list))
    imgA = imread(fullfile(list(i).folder, list(i).name));
    [xs, ys, zs] = size(imgA);
    
    % split
    for j = 1:floor(xs/(patch_size-overlap))
        for k = 1:floor(ys/(patch_size-overlap))
            
            xi = 1+(j-1)*(patch_size-overlap);
            yi = 1+(k-1)*(patch_size-overlap);
            
            img = imgA(xi:xi+patch_size-1,yi:yi+patch_size-1,:);
            
            imwrite(img, ['./testB-GT/file' num2str(i) '_' num2str(xi) '_' num2str(yi) '_' num2str(xs) '_' num2str(ys) '_' num2str(patch_size) '_' num2str(overlap) '_.tif']);
        end
    end
    
end