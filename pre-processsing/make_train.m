clc;clear;

patch_size = 256;
nb_per_slide = 1000;

folderA = './raw/trainA_whole/';
folderB = './raw/trainB_whole/';
%% for A
list = dir([folderA '*.tif']);
k = 0;
for ii = 1:length(list)
    
    fprintf('%d of %d...\n', ii, length(list))
    img = loadtiff(fullfile(list(ii).folder, list(ii).name));
    
    [xs,ys,~] = size(img);
    nb_per_slide = floor(xs*ys/7000);
    
    % cord
    cord = zeros((xs-patch_size+1)*(ys-patch_size+1), 2);
    for i = 1:(xs-patch_size+1)
        for j = 1:(ys-patch_size+1)
            
            cord(j+(i-1)*(ys-patch_size+1), 1) = i;
            cord(j+(i-1)*(ys-patch_size+1), 2) = j;
            
        end
    end
    
    %
    sp = randperm(size(cord, 1), nb_per_slide);
    for j = 1:nb_per_slide
        k=k+1;
        xi = cord(sp(j), 1);
        yi = cord(sp(j), 2);
        imgP = img(xi:xi+patch_size-1,yi:yi+patch_size-1,:);
        
        saveastiff(imgP, ['./trainA/' num2str(k) '.tif']);
    end
end


%% for B
list = dir([folderB '*.png']);
k = 0;
for ii = 1:length(list)
    
    fprintf('%d of %d...\n', ii, length(list))
    img = imread(fullfile(list(ii).folder, list(ii).name));
    
    [xs,ys,~] = size(img);
    nb_per_slide = floor(xs*ys/7000);
    
    % cord
    cord = zeros((xs-patch_size+1)*(ys-patch_size+1), 2);
    for i = 1:(xs-patch_size+1)
        for j = 1:(ys-patch_size+1)
            
            cord(j+(i-1)*(ys-patch_size+1), 1) = i;
            cord(j+(i-1)*(ys-patch_size+1), 2) = j;
            
        end
    end
    
    %
    sp = randperm(size(cord, 1), nb_per_slide);
    for j = 1:nb_per_slide
        k=k+1;
        xi = cord(sp(j), 1);
        yi = cord(sp(j), 2);
        imgP = img(xi:xi+patch_size-1,yi:yi+patch_size-1,:);
        
        imwrite(imgP, ['./trainB/' num2str(k) '.tif']);
    end
end