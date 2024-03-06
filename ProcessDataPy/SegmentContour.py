#计算等高线顶点的转角和曲率特征。输入等高线，输出带特征的顶点(# Calculate the corner and curvature characteristics of contour vertices. Input contours, output vertices with features)
def CalVerticeCornerCurvature(pathContour,pathVertices):
    try:
        import time  # 导入time模块        
        import geopandas as gpd
        from shapely.geometry import Point
        import math

        # 读取等高线数据
        contour_gdf = gpd.read_file(pathContour)

        # 创建一个空的 GeoDataFrame 用于保存顶点
        point_gdf = gpd.GeoDataFrame(columns=["OBJECTID", "corner", "curvature"], geometry=[],crs= contour_gdf.crs)

        # 遍历等高线并计算转角和曲率
        pntID=0
        start_time = time.time()  # 记录开始时间
        for idx, row in contour_gdf.iterrows():
            line = row["geometry"]
            if line.is_valid:  # 仅处理有效几何体
                coords = line.coords

                for i in range(1, len(coords) - 1):
                    pntID=pntID+1
                    pi = Point(coords[i - 1])
                    pj = Point(coords[i])
                    pk = Point(coords[i + 1])

                    edgei = pi.distance(pk)
                    edgej = pj.distance(pk)
                    edgek = pi.distance(pj)
                    edgei = math.sqrt((pj.x - pk.x) * (pj.x - pk.x) + (pj.y - pk.y) * (pj.y - pk.y))
                    edgej = math.sqrt((pi.x - pk.x) * (pi.x - pk.x) + (pi.y - pk.y) * (pi.y - pk.y))
                    edgek = math.sqrt((pi.x - pj.x) * (pi.x - pj.x) + (pi.y - pj.y) * (pi.y - pj.y))
                    cos_value = ((pj.x - pi.x) * (pk.x - pj.x) + (pj.y - pi.y) * (pk.y - pj.y)) / (edgei * edgek)
                    if -1 <= cos_value <= 1:
                        cornerj = math.degrees(math.acos(cos_value))
                        len_j1orderAdj = edgei + edgek
                        curvaturej = cornerj / len_j1orderAdj
                        point_gdf = point_gdf.append({"OBJECTID": pntID, "corner": cornerj, "curvature": curvaturej, "geometry": pj}, ignore_index=True)
                    else:
                        # 处理参数值超出有效范围的情况
                        print("Invalid cosine value:", cos_value)
            else:
                print(row["OBJECTID"])
            elapsed_time = time.time() - start_time
            if elapsed_time >= 30:  # 如果已经过去30秒
                print(f"已运行 {int(elapsed_time)} 秒,已计算{int(pntID)}个点")
                start_time = time.time()  # 重置开始时间                
        # 保存顶点数据
        point_gdf.to_file(pathVertices)
    except Exception as e:
        print(f"发生异常：{str(e)}")

    print("完成！输出带转角曲率特征的顶点图层")

## 输入等高线的顶点，输出分段点
## pathVertices是等高线顶点shp，顶点带有转角字段；pathSegLines在分段点处建立的线段shp；
## segValue是分段阈值；angle和line_length：分段点处建立的线段的方向和长度
## Input the vertex of the contour line and output the segment point
## pathVertices are contour vertices shp with corner fields; pathSegLines shp established at the segment point;
## segValue is the segmentation threshold; angle and line_length: The direction and length of the line segment established at the segment point
def outPutSegPnt(pathVertices,pathSegVertices,pathSegLines=None,segValue=60,angle = 37.711,line_length = 20):
    try:
        import time  # 导入time模块        
        import geopandas as gpd
        from shapely.geometry import Point, LineString
        from shapely.ops import split
        import math
        # 读取点图层
        points_gdf = gpd.read_file(pathVertices)
        # 创建一个空的 GeoDataFrame 用于保存顶点
        SegPoint_gdf = gpd.GeoDataFrame(columns=["OBJECTID", "corner", "curvature"], geometry=[],crs= points_gdf.crs)        
        # # 创建一个空的 GeoDataFrame 用于保存新的线段
        # lines_gdf = gpd.GeoDataFrame(columns=["OBJECTID"], geometry=[], crs=points_gdf.crs)
        # 遍历点图层并创建新线段
        newline_index=0
        start_time = time.time()  # 记录开始时间
        for index, row in points_gdf.iterrows():
            corner_value = row["corner"]
            # 检查 corner 值是否大于segValue度
            if corner_value >= segValue:
                point_geometry = row["geometry"]
                SegPoint_gdf=SegPoint_gdf.append({"OBJECTID": index, "corner": corner_value, "curvature": row["curvature"], "geometry": point_geometry}, ignore_index=True)
                
                # 创建一个新线段，方向角度为angle， 长度为line_lengthm，中心为顶点
                # 计算新线段的两个端点
                start_x = point_geometry.x - (line_length / 2) * math.cos(math.radians(angle))
                start_y = point_geometry.y - (line_length / 2) * math.sin(math.radians(angle))
                end_x = point_geometry.x + (line_length / 2) * math.cos(math.radians(angle))
                end_y = point_geometry.y + (line_length / 2) * math.sin(math.radians(angle))
                new_line = LineString([(start_x, start_y), (end_x, end_y)])
                # # 将新线段添加到新的线图层
                # lines_gdf = lines_gdf.append({"OBJECTID": newline_index, "geometry": new_line}, ignore_index=True)
                # newline_index=newline_index+1
            elapsed_time = time.time() - start_time
            if elapsed_time >= 30:  # 如果已经过去30秒
                print(f"已运行 {int(elapsed_time)} 秒")
                start_time = time.time()  # 重置开始时间         
        # 保存分段点的图层
        SegPoint_gdf.to_file(pathSegVertices)
        # # 保存新的线图层
        # lines_gdf.to_file(pathSegLines)
    except Exception as e:
        print(f"发生异常：{str(e)}")
    print("完成！输出分段点、线图层")

import geopandas as gpd
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points

#获得从断头点到最近点的线段(# Get the line segment from the broken point to the nearest point)
def getLineFromBrokenPntToNearestPnt(start_point,contour_gdf, buffer_radius_large, id_line,elev):
    # 创建1米半径的圆形缓冲区
    buffer_radius = 1  # 单位为米
    buffer_area = start_point.buffer(buffer_radius)
    # 找到与圆形缓冲区相交的等高线
    intersecting_contours = contour_gdf[contour_gdf.intersects(buffer_area)]     
    if len(intersecting_contours)<=1:
        # 创建1000米半径的圆形缓冲区
        buffer_area_large = start_point.buffer(buffer_radius_large)
        # 找到与圆形缓冲区相交的等高线
        intersecting_contours_inBuffer = contour_gdf[contour_gdf.intersects(buffer_area_large)]  
        nearest_distance = float('inf')
        nearest_point = None                          
        for index_inBuffer, row_inBuffer in intersecting_contours_inBuffer.iterrows():   
            id_line_inBuffer=row_inBuffer["OBJECTID"]    
            elv_inBuffer=row_inBuffer["Contour"]      
            if id_line_inBuffer == id_line or elev==elv_inBuffer or int(abs(elev-elv_inBuffer))!=20:
                continue
            else:
                # 找到等高线 上距离断头点 最近的点
                line1 = row_inBuffer['geometry']
                # 使用nearest_points函数找到线上最近的点
                closest_point = nearest_points(line1, start_point)
                # closest_point是一个包含两个点的元组，取第二个点即为距离点p最近的线上的点
                nearest_point_on_line = closest_point[0]        
                distance = start_point.distance(nearest_point_on_line)
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_point = nearest_point_on_line
            new_line = LineString([(start_point.x, start_point.y), (nearest_point.x, nearest_point.y)])

        if nearest_point is None:
            # 创建2000米半径的圆形缓冲区
            buffer_area_large = start_point.buffer(2*buffer_radius_large)
            # 找到与圆形缓冲区相交的等高线
            intersecting_contours_inBuffer = contour_gdf[contour_gdf.intersects(buffer_area_large)]  
            nearest_distance = float('inf')
            nearest_point = None                          
            for index_inBuffer, row_inBuffer in intersecting_contours_inBuffer.iterrows():   
                id_line_inBuffer=row_inBuffer["OBJECTID"]          
                elv_inBuffer=row_inBuffer["Contour"]      
                if id_line_inBuffer == id_line or elev==elv_inBuffer:
                    continue
                else:
                    # 找到等高线 上距离断头点 最近的点
                    line1 = row_inBuffer['geometry']
                    # 使用nearest_points函数找到线上最近的点
                    closest_point = nearest_points(line1, start_point)
                    # closest_point是一个包含两个点的元组，取第二个点即为距离点p最近的线上的点
                    nearest_point_on_line = closest_point[0]    
                    distance = start_point.distance(nearest_point_on_line)
                    if distance < nearest_distance:
                        nearest_distance = distance
                        nearest_point = nearest_point_on_line               
            new_line = LineString([(start_point.x, start_point.y), (nearest_point.x, nearest_point.y)])
        return new_line
    else:
        return None

#处理断头线：输入分段后的等高线，输出断头点，再找到距离断头点最近的点，输出新建线。(# Process the broken line: input the contour line after the segmentation, output the broken point, and then find the point closest to the broken point, output a new line.)
def processBrokenLins(path_contour,pathBrokenPnt,buffer_radius_large,path_contourNoBrokenLine):
    try:
        import geopandas as gpd
        from shapely.geometry import Point, LineString
        # 读取等高线数据
        contour_gdf = gpd.read_file(path_contour)
        # 创建一个新的GeoDataFrame用于保存非断头线
        contour_brokenPnt_gdf = gpd.GeoDataFrame(columns=["OBJECTID", "geometry"], geometry=[],crs= contour_gdf.crs)
        # 创建一个新的GeoDataFrame用于保存非断头线
        contour_no_broken_gdf = gpd.GeoDataFrame(columns=["OBJECTID", "geometry"], geometry=[],crs= contour_gdf.crs)
                
        ##找到断头点
        id_brokenPnt=0
        caledPnt=[]#已经计算过的点
        # 遍历等高线数据
        for index, row in contour_gdf.iterrows():
            line = row["geometry"]
            id_line=row["OBJECTID"]
            elev=row["Contour"]
            coords = list(line.coords)
            start_point = Point(coords[0])
            end_point = Point(coords[-1])   
            if start_point not in caledPnt:
                caledPnt.append(start_point)
                # 创建1米半径的圆形缓冲区
                buffer_radius = 1  # 单位为米
                buffer_area = start_point.buffer(buffer_radius)
                # 找到与圆形缓冲区相交的等高线
                intersecting_contours = contour_gdf[contour_gdf.intersects(buffer_area)]     
                if len(intersecting_contours)<=1:    
                    contour_brokenPnt_gdf = contour_brokenPnt_gdf.append({"OBJECTID": id_brokenPnt, "geometry": start_point}, ignore_index=True)     
                    id_brokenPnt=id_brokenPnt+1           
                    new_line=getLineFromBrokenPntToNearestPnt(start_point,contour_gdf,buffer_radius_large,id_line,elev)
                    if new_line is not None:

                        # 如果新线段是多部分几何，拆分成单独的几何对象
                        if new_line.geom_type == 'MultiLineString':
                            for geom in new_line:
                                contour_no_broken_gdf = contour_no_broken_gdf.append({"OBJECTID": id_line, "geometry": geom}, ignore_index=True)
                        else:
                            contour_no_broken_gdf = contour_no_broken_gdf.append({"OBJECTID": id_line, "geometry": new_line}, ignore_index=True)
                                
            start_point = end_point
            if start_point not in caledPnt:
                caledPnt.append(start_point)
                # 创建1米半径的圆形缓冲区
                buffer_radius = 1  # 单位为米
                buffer_area = start_point.buffer(buffer_radius)
                # 找到与圆形缓冲区相交的等高线
                intersecting_contours = contour_gdf[contour_gdf.intersects(buffer_area)]     
                if len(intersecting_contours)<=1:
                    contour_brokenPnt_gdf = contour_brokenPnt_gdf.append({"OBJECTID": id_brokenPnt, "geometry": start_point}, ignore_index=True)     
                    id_brokenPnt=id_brokenPnt+1                      
                    new_line=getLineFromBrokenPntToNearestPnt(start_point,contour_gdf,buffer_radius_large,id_line,elev)
                    if new_line is not None:
                        
                        # 如果新线段是多部分几何，拆分成单独的几何对象
                        if new_line.geom_type == 'MultiLineString':
                            for geom in new_line:
                                contour_no_broken_gdf = contour_no_broken_gdf.append({"OBJECTID": id_line, "geometry": geom}, ignore_index=True)
                        else:
                            contour_no_broken_gdf = contour_no_broken_gdf.append({"OBJECTID": id_line, "geometry": new_line}, ignore_index=True)                        
        #保存断头点
        contour_brokenPnt_gdf.to_file(pathBrokenPnt)        
        contour_no_broken_gdf = contour_no_broken_gdf.append(contour_gdf, ignore_index=True)
        # 保存非断头线和新线段到contourNoBrokenLine.shp
        contour_no_broken_gdf.to_file(path_contourNoBrokenLine)
    except Exception as e:
        print(f"发生异常：{str(e)}")
    print("完成！生成无断头线图层")                        
                                
        ##再找到距离断头点最近的点，新建线。

#####程序入口  （program entry）
#计算等高线顶点的特征，并输出顶点shp(# Calculate the features of the contour vertices and output the vertex shp)
# pathContour=r"\0datasource\shp\SkyContourChunHua单部件Gen100m.shp"    
# pathVertices=r"\0datasource\shp\SkyContourChunHuaSinglePartVertices.shp"
pathContour=r"0datasource\shp\陕北等高线\延安20mGen100m.shp"
pathVertices=r"0datasource\shp\陕北等高线\延安20mGen100mVertice.shp"
CalVerticeCornerCurvature(pathContour,pathVertices) 
  
# # 从顶点shp找出分段点，并分段等高线（# # Find the segment points from the vertex shp and segment the contours）
# pathVertices=r"\0datasource\shp\SkyContourChunHuaSinglePartVertices.shp"
# pathSegVertices=r"\0datasource\shp\SkyContourChunHuaSinglePartSegVertices60度.shp"
# pathSegLines=r"\0datasource\shp\咸阳等高线\Contour淳化WGSprj20m单部件长于100mGen100mSegLinesForSeg60度.shp"
pathVertices=r"0datasource\shp\陕北等高线\延安20mGen100mVertice.shp"
pathSegVertices=r"0datasource\shp\陕北等高线\延安20mGen100mVerticeSeg.shp"
segValue=60#分段的阈值：顶点的转角大于等于segValue，被视为分段点(Segmentation threshold: The Angle of the vertex is greater than or equal to the segValue, which is regarded as the segmentation point)
outPutSegPnt(pathVertices,pathSegVertices,segValue)

##------------------
##在qgis用分段点打断等高线：split lines at points(## In qgis break contour lines with segment points: split lines at points)
##------------------


# ##处理断头线【1029结果不好，暂时不用】
# buffer_radius_large = 1000  # 单位为米
# path_contour=r"\0datasource\shp\SkyContourChunHuaYuanTest.shp"
# pathBrokenPnt=r"\0datasource\shp\SkyContourChunHuaYuanTestBrokenPnt.shp"
# path_contourNoBrokenLine=r"\0datasource\shp\SkyContourChunHuaYuanTestNoBrokenLine.shp"
# processBrokenLins(path_contour,pathBrokenPnt,buffer_radius_large,path_contourNoBrokenLine)                               
