import os
import cv2


path=r"C:\Users\deepa\Downloads\hfh\NNNNNNNNNNNNNNNNNN"
dest_path=r"C:\Users\deepa\Downloads\hfh\NNNNNNNNNNNNNNNNNN\new_label"
p=0
def draw_rec(pts,image,z):
    global p
    for pt in pts:
        # print(pt)
        # Start coordinate, here (5, 5) 
        # represents the top left corner of rectangle 
        start_point = (int(pt[0]), int(pt[1])) 
        
        # Ending coordinate, here (220, 220) 
        # represents the bottom right corner of rectangle 
        end_point = (int(pt[2]), int(pt[3]))
        
        # Blue color in BGR 
        color = (255, 0, 0) 
        
        # Line thickness of 2 px 
        thickness = 4
        
        # Using cv2.rectangle() method 
        # Draw a rectangle with blue line borders of thickness of 2 px 
        image = cv2.rectangle(image, start_point, end_point, color, thickness)
    if z==1:
        file_name=f"C:/Users/deepa/Downloads/hfh/NNNNNNNNNNNNNNNNNN/raw/image_{p}.jpg"
    else:
        file_name=f"{dest_path}/image_{p}.jpg"
    cv2.imwrite(file_name,image) 
    p+=1
 


def area_bbox(bbox,dim):
    area_bb=(bbox[2]-bbox[0])*(bbox[3]-bbox[1])
    print(area_bb)
    if area_bb>=29000:
        return True
    else:
        return False
    
    
    
def change_cordinates(file,dim,image):
    image2=image
    copy_bb=[]
    all_point=[]
    main_point=[]
    for i in file:
        cls,x,y,w,h=i.split(" ")
        x,y,w,h=float(x),float(y),float(w),float(h)
        absolute_x=x*dim[0]
        absolute_y=y*dim[1]
        absolute_width=w*dim[0]
        absolute_height=h*dim[1]  
        xmin=int(absolute_x-(0.5*absolute_width))
        ymin=int(absolute_y-(0.5*absolute_height))
        xmax=int(absolute_width+xmin)
        ymax=int(absolute_height+ymin)
        all_point.append([xmin,ymin,xmax,ymax])
        val=area_bbox([xmin,ymin,xmax,ymax],dim)
        # print(xmin,xmax,ymin,ymax)
        if val:
            copy_bb.append(i)
            main_point.append([xmin,ymin,xmax,ymax])
    draw_rec(main_point,image2,z=1)
    draw_rec(all_point,image,z=2)
    return (copy_bb)


def read_img_txt():
    img_path=path+"/image"
    for img in os.listdir(img_path):
        im_path=img_path+"/"+img
        print(im_path)
        image=cv2.imread(im_path)
        height,width,c=image.shape
        txt_path=path+"/label/"+os.path.splitext(img)[0]+".txt"
        with open(txt_path,"r") as files:
              file=files.readlines()    
        txt_list=change_cordinates(file,(width,height),image)
        new_txt_path=dest_path+"/"+os.path.splitext(img)[0]+".txt"
        with open(new_txt_path,"w") as f:
            f.writelines(txt_list)
            
            
read_img_txt()
