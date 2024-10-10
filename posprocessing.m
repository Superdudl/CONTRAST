clc
clear
close all

img = imread("tst_img.bmp");
[h, w] = size(img);
fig = figure(1);
imshow(img)

figure(2)
histogram(img, 32);

number_low = img > 70;
number_hight = img < 100;
numbers_mask = uint8(number_low.*number_hight);

paper_low = img > 120;
paper_hight = img < 230;
paper_mask = uint8(paper_low.*paper_hight);


paper_img = img.*paper_mask;
numbers_img = img.*numbers_mask;

imshow(cat(2, numbers_img, uint8(255*ones(h, 30)) ,paper_img))
