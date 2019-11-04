clc;clear;
imgsA = loadtiff('liver-A.tif');
imgsB = loadtiff('liver-B.tif');

patch_size = 128;
overlap = 16;
[xs,ys,zs] = size(imgsA);

%% for A
for i = 1:20
    % slide norm
    imgA = imgsA(:,:,i);
    imgA = double(imgA);
    imgA = imgA - min(imgA(:));
    imgA = imgA/max(imgA(:));
    imgA = uint8(255*imgA);
    
    %     imwrite(imgA, ['./test-whole-slide/testA/' num2str(i) '.png'] )
    
    % split
    for j = 1:floor(xs/(patch_size-overlap))
        for k = 1:floor(ys/(patch_size-overlap))
            xi = 1+(j-1)*(patch_size-overlap);
            yi = 1+(k-1)*(patch_size-overlap);
            
            img = imgA(xi:xi+patch_size-1,yi:yi+patch_size-1);
            
            imwrite(img, ['./testA/' num2str(i) '_' num2str(xi) '_' num2str(yi) '_' num2str(xs) '_' num2str(ys) '_' num2str(patch_size) '_' num2str(overlap) '_.png']);
        end
    end
    
end

%% for B
for i = 1:20
    % slide norm
    imgB = imgsB(:,:,i);
    imgB = double(imgB);
    imgB = imgB - min(imgB(:));
    imgB = imgB/max(imgB(:));
    imgB = uint8(255*imgB);
    
    %     imwrite(imgB, ['./test-whole-slide/GT/' num2str(i) '.png'] )
    
    % split
    for j = 1:floor(xs/(patch_size-overlap))
        for k = 1:floor(ys/(patch_size-overlap))
            xi = 1+(j-1)*(patch_size-overlap);
            yi = 1+(k-1)*(patch_size-overlap);
            img = imgB(xi:xi+patch_size-1,yi:yi+patch_size-1);
            
            imwrite(img, ['./testB-GT/' num2str(i) '_' num2str(xi) '_' num2str(yi) '_' num2str(xs) '_' num2str(ys) '_' num2str(patch_size) '_' num2str(overlap) '_.png']);
        end
    end
    
end