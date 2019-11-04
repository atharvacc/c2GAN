clc;clear;
imgsA = loadtiff('liver-A.tif');
imgsB = loadtiff('liver-B.tif');
patch_size = 128;
nb_per_slide = 200;
[xs,ys,zs] = size(imgsA);

% img cord
cord = zeros((xs-patch_size+1)*(ys-patch_size+1), 2);
for i = 1:(xs-patch_size+1)
    for j = 1:(ys-patch_size+1)
        
       cord(j+(i-1)*(ys-patch_size+1), 1) = i;
       cord(j+(i-1)*(ys-patch_size+1), 2) = j;
        
    end
end

%% for A
k=0;
for i = 21:zs
    i
    % slide norm
    imgA = imgsA(:,:,i);
    imgA = double(imgA);
    imgA = imgA - min(imgA(:));
    imgA = imgA/max(imgA(:));
    imgA = uint8(255*imgA);
    
    % split
    sp = randperm(size(cord, 1), nb_per_slide);
    for j = 1:nb_per_slide
        k=k+1;
        xi = cord(sp(j), 1);
        yi = cord(sp(j), 2);
        img = imgA(xi:xi+patch_size-1,yi:yi+patch_size-1);
        
        imwrite(img, ['./trainA/' num2str(k) '.png']);
    end
    
end

%% for B
k=0;
for i = 21:zs
    i
    % slide norm
    imgB = imgsB(:,:,i);
    imgB = double(imgB);
    imgB = imgB - min(imgB(:));
    imgB = imgB/max(imgB(:));
    imgB = uint8(255*imgB);
    
    % split
    sp = randperm(size(cord, 1), nb_per_slide);
    for j = 1:nb_per_slide
        k=k+1;
        xi = cord(sp(j), 1);
        yi = cord(sp(j), 2);
        img = imgB(xi:xi+patch_size-1,yi:yi+patch_size-1);
        
        imwrite(img, ['./trainB/' num2str(k) '.png']);
    end
    
end