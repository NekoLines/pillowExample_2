
# coding=utf-8
# 引入必须的库文件
from PIL import Image,ImageDraw,ImageFont
from datetime import date, datetime
from zhdate import ZhDate

def get_date_nl_chinese(datetime):
    date = ZhDate.from_datetime(datetime)
    nl = date.chinese()
    nl = nl.split("年")
    nl = nl[1].split("月")
    mm = nl[0]
    nl = nl[1].split(" ")[0]
    if nl == "初一":
        return str(mm+"月")[0:2]
    else:
        return nl[0:2]

def make_paiban_pic_n(year,month,month_list,filename):
   # 设置字体，这里选择了霞鹜文楷
    font_month = ImageFont.truetype("LXGWWenKaiMonoTC-Regular.ttf", 50)
    font_nl = ImageFont.truetype("LXGWWenKaiMonoTC-Regular.ttf", 20)
    font_zb = ImageFont.truetype("LXGWWenKaiMonoTC-Regular.ttf", 30)
    # 新建一个背景文件，把 Draw 对象初始化
    background = Image.new(mode = 'RGBA',size = (500,500),color = 'white')
    draw = ImageDraw.Draw(background)
    # 通过 textSize 函数获取文字所占面积
    zbw,zbh = draw.textsize("今日值班", font=font_zb, spacing=6)
    nlw,nlh = draw.textsize("值\n班", font=font_nl, spacing=6)
    mtw,mth = draw.textsize("30", font=font_month, spacing=6)

    color_blue = (71,124,246)
    color_black = (26,26,26)
    color_grey = (130,130,130)
    color_green = (140,192,97)
    color_red = (224,102,75)
    color_white = (255,255,255)

    height_jg = 45
    width_jg = 30

    date_size_w = zbw + 16;
    date_size_h = nlh + 15 + zbh + 16

    img_w = date_size_w * 7 + width_jg * 8
    img_h = mth + zbh + date_size_h * len(month_list) + (len(month_list)+3) * height_jg

    img_size = (img_w,img_h)

    background = background.resize(img_size,Image.ANTIALIAS)

    draw = ImageDraw.Draw(background)

    # 描绘标题
    draw.text((width_jg,height_jg), str(year)+"-"+str(month)+"月工作情况", fill=(0,0,0), font=font_month)

    #描绘周几标题
    week_list = ["周日","周一","周二","周三","周四","周五","周六"]
    for i in range(0,7):
        tmp_size_width,tmp_size_heigth = draw.textsize(week_list[i], font=font_zb, spacing=6)
        bq = ((date_size_w - tmp_size_width)/2) if tmp_size_width < date_size_w else 0;
        draw.text((width_jg * ( i + 1 )+ date_size_w * i + bq+10,height_jg * 2 + mth), week_list[i], fill=(0,0,0), font=font_nl)

    #描绘日期
    for w in range(0,len(month_list)):         
        week = month_list[w]
        for i in range(0,len(week)):
            day = week[i]
            day_status = "值班" if day[1] else "休息"
            if day[2]!="":
                day_m = str(day[0])
                day_nl = str(day[2][0:1]+"\n"+day[2][-1:])
                
                zbw,zbh = draw.textsize(day_status, font=font_zb, spacing=6)
                nlw,nlh = draw.textsize(day_nl, font=font_nl, spacing=6)
                mtw,mth = draw.textsize(day_m, font=font_month, spacing=6)

                #确定x，y
                x,y = (width_jg * ( i + 1 )+ date_size_w * i,height_jg * ( w + 3 ) + mth + date_size_h * w )
                dxpd,dypd = (date_size_w - mtw)/2,(date_size_h - zbh - 16-mth)/2-15
                nlx,nly = (date_size_w - dxpd+mtw-nlw)/2+x+dxpd,(date_size_h-zbh-16-nlh)/2+y-13
                rect_x,rect_y,rect_w,rect_h=x,y+date_size_h-zbh-16,date_size_w,zbh+16
                zbx,zby = x + (date_size_w-zbw)/2,rect_y+(rect_h-zbh)/2
                if day[1]:
                    month_fill_color = color_black
                    rect_fill_color = color_blue
                elif i == 0 or i == 6:
                    month_fill_color = color_red
                    rect_fill_color = color_red
                else:
                    month_fill_color = color_black
                    rect_fill_color = color_green                

                draw.text((nlx,nly),day_nl,fill=color_grey,font=font_nl)
                draw.text((x + dxpd,y+dypd), day_m, fill=month_fill_color, font=font_month)
                drawRoundRec(background,draw,rect_fill_color,rect_x,rect_y,rect_w,rect_h,15)
                draw.text((zbx,zby),day_status,fill=color_white,font=font_zb)

    background.save(filename)

def get_month_daysnum(year,month):
    if month in [1,3,5,7,8,10,12]:
        return 31
    elif month in [4,6,9,11]:
        return 30
    elif month == 2:
        if (year % 4 == 0 and year % 100 != 0)or year % 400 == 0:
            return 29
        else:
            return 28
    else:
        return -1 
    
def make_paiban_list(year,month,start_day,ls_day,rest_day):
    count_day = get_month_daysnum(year,month)
    start_week = date(year, month, 1).weekday()
    print(start_week)
    date_week_list_tmp = [1,2,3,4,5,6,0]
    flag = date_week_list_tmp[start_week]
    month_lists = []
    tmp_list = []
    isWork = False
    flag_day = -1
    tmp_ls = -1
    for i in range(0-flag,count_day):
        if len(tmp_list) > 6:
            month_lists.append(tmp_list)
            tmp_list = []
        if i < 0:
            tmp_list.append([" ",False,""])
        else:
            if i+1 == start_day or flag_day == 0:
                isWork = True
                flag_day = rest_day
                tmp_ls = ls_day - 1
            elif tmp_ls > 0:
                tmp_ls = tmp_ls - 1
                isWork = True
            else:
                flag_day = flag_day - 1
                isWork = False
            tmp_list.append([str(i+1),isWork,get_date_nl_chinese(datetime(year,month,i+1))])
    if len(tmp_list) != 0:
        for i in range(len(tmp_list),7):
            tmp_list.append([" ",False,""])
        month_lists.append(tmp_list)
    return month_lists

def drawRoundRec(im,drawObject, color, x, y, w, h, r):
    '''Rounds'''    
    drawObject.ellipse((x,y,x+r,y+r),fill=color)    
    drawObject.ellipse((x+w-r,y,x+w,y+r),fill=color)    
    drawObject.ellipse((x,y+h-r,x+r,y+h),fill=color)    
    drawObject.ellipse((x+w-r,y+h-r,x+w,y+h),fill=color)
    '''rec.s'''    
    drawObject.rectangle((x+r/2,y, x+w-(r/2), y+h),fill=color)    
    drawObject.rectangle((x,y+r/2, x+w, y+h-(r/2)),fill=color)


if __name__ == "__main__":
    year = 2022
    month = 8
    list = make_paiban_list(year,month,1,1,2)
    print(list)
    make_paiban_pic_n(year,month,list,str(year)+"-"+str(month)+".png")