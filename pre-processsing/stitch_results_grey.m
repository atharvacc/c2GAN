clc;clear;
% stitch test results together
% overlap should be set

patch_size = 128;
overlap = 16;
fntif = './testB/';
fnrlt = './test-whole-slide/';

% get the list of all slides
list = dir([fntif '*.png']);

% figure out how many slides in the folder
raw_name = list(end).name;
% cell_str = strsplit(raw_name, '_');
cell_str = strsplit(raw_name(4:end-13), '_');
zs = str2num(cell_str{1});
xs = str2num(cell_str{4});
ys = str2num(cell_str{5});
% buffer
img_rlt = zeros(xs,ys,zs,'uint8');

%% do stitching
for i = 1:length(list)
    % stitching
    if mod(i, 100) ==0
        fprintf('Progress %d of %d ...\n', i, length(list))
    end
    
    img = imread(fullfile(list(i).folder, list(i).name));
    
    % get slide info;
    raw_name = list(i).name;
    cell_str = strsplit(raw_name(4:end-13), '_');
    %     cell_str = strsplit(raw_name, '_');
    
    z = str2num(cell_str{1});
    xi = str2num(cell_str{2});
    yi = str2num(cell_str{3});
    % get start index
    xidx = xi+overlap/2;
    yidx = yi+overlap/2;
    
    img_rlt(xidx:xidx+patch_size-overlap-1, yidx:yidx+patch_size-overlap-1, z) = img(overlap/2+1:end-overlap/2,overlap/2+1:end-overlap/2);
    
end

% save image
fprintf('Save as %s.\n', [fnrlt 'B.tif'])
saveastiff(img_rlt, [fnrlt 'B.tif']);


