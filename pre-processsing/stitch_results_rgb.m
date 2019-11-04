clc;clear;
% stitch test results together
% overlap should be set

patch_size = 256;
overlap = 32;
fntif = './testB-1/';
fnrlt = './test-whole-slide/';

img_gt = im2uint8(loadtiff('./test-whole-slide/GT.tif'));

% get the list of all slides
list = dir([fntif '*.png']);

% figure out how many slides in the folder
raw_name = list(end).name;
% cell_str = strsplit(raw_name, '_');
cell_str = strsplit(raw_name(8:end-13), '_');
zs = 3;
xs = str2num(cell_str{4});
ys = str2num(cell_str{5});
% buffer
img_rlt = zeros(xs,ys,zs,'uint8');

weight_mask = 0.5 * ones(patch_size, patch_size);
weight_mask_1 = ones(patch_size-2*overlap, patch_size-2*overlap);
weight_mask(overlap+1:end-overlap, overlap+1:end-overlap) = weight_mask_1;

%% do stitching
for ii = 1:length(list)
    % stitching
    if mod(ii, 100) ==0
        fprintf('Progress %d of %d ...\n', ii, length(list))
    end
    
    img = imread(fullfile(list(ii).folder, list(ii).name));
    %     img = uint8(mean(double(img), 3));
    
    % get slide info;
    raw_name = list(ii).name;
    cell_str = strsplit(raw_name(8:end-13), '_');
    %     cell_str = strsplit(raw_name, '_');
    
    %     z = str2num(cell_str{1});
    xi = str2num(cell_str{2});
    yi = str2num(cell_str{3});
    % get start index
    xidx = xi+overlap/2;
    yidx = yi+overlap/2;
    
    imgP_gt = img_gt(xidx:xidx+patch_size-overlap-1, yidx:yidx+patch_size-overlap-1, :);
    imgP_net = img(overlap/2+1:end-overlap/2,overlap/2+1:end-overlap/2,:);
    
    imgP_gt = double(imgP_gt);    
    imgP_net = double(imgP_net);
    
    
    for i = 1:3
        
        % normalization
        imgP_net(:,:,i) = imgP_net(:,:,i)-min(min(imgP_net(:,:,i)));
        imgP_net(:,:,i) = imgP_net(:,:,i)/max(max(imgP_net(:,:,i)));
        
        % stretch
        imgP_net(:,:,i) = imgP_net(:,:,i) * (max(max(imgP_gt(:,:,i))) - min(min(imgP_gt(:,:,i))));
        imgP_net(:,:,i) = imgP_net(:,:,i) + min(min(imgP_gt(:,:,i)));
        
%         imgP_net(:,:,i) = imgP_net(:,:,i) * (mean(mean(imgP_gt(:,:,i)))/mean(mean(imgP_net(:,:,i))));
        
        
    end
    
    img_rlt(xidx:xidx+patch_size-overlap-1, yidx:yidx+patch_size-overlap-1, :) = imgP_net;
    
    
end


% save image
fprintf('Save as %s.\n', [fnrlt 'B.tif'])
imwrite(img_rlt, [fnrlt 'B.tif']);

