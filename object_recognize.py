import pcl
import numpy as np
import PSpincalc as sp

def downSample(cloud, length, width, high):
    length_pass = cloud.make_passthrough_filter()
    length_pass.set_filter_field_name('x')
    length_pass.set_filter_limits(-length/2, length/2)
    cloud_length_pass = length_pass.filter()
    width_pass = cloud_length_pass.make_passthrough_filter()
    width_pass.set_filter_field_name('y')
    width_pass.set_filter_limits(-width/2, width/2)
    cloud_width_pass = width_pass.filter()
    high_pass = cloud_width_pass.make_passthrough_filter()
    high_pass.set_filter_field_name('z')
    high_pass.set_filter_limits(-high/2, high/2)
    cloud_high_pass = high_pass.filter()
    return cloud_width_pass
def do_euclidean_clustering(white_cloud):
    '''
    :param cloud_objects:
    :return: cluster cloud and cluster indices
    '''
    tree = white_cloud.make_kdtree()
    # Create Cluster-Mask Point Cloud to visualize each cluster separately
    ec = white_cloud.make_EuclideanClusterExtraction()
    ec.set_ClusterTolerance(0.10)
    # ec.set_MinClusterSize(20000)
    #    ec.set_MinClusterSize(20000)
    #    ec.set_MaxClusterSize(60000)
    ec.set_MinClusterSize(100)
    ec.set_MaxClusterSize(600)
    ec.set_SearchMethod(tree)
    cluster_indices = ec.Extract()
    # cluster_color = get_color_list(len(cluster_indices))
    color_cluster_point_list = []
    # for j, indices in enumerate(cluster_indices):
    cluster_cloud = pcl.PointCloud()
    if len(cluster_indices) == 0:
        return cluster_cloud, cluster_indices
    for indice in cluster_indices[0]:
        # for i, indice in enumerate(indices):
        #     color_cluster_point_list.append([white_cloud[indice][0], white_cloud[indice][1], white_cloud[indice][2], rgb_to_float(cluster_color[j])])
        color_cluster_point_list.append([white_cloud[indice][0], white_cloud[indice][1], white_cloud[indice][2]])
    cluster_cloud.from_list(color_cluster_point_list)
    return cluster_cloud,cluster_indices

def ModelPlane(cloud_filter, threshold=0.1 ,ext=True):
    modle_p = pcl.SampleConsensusModelPlane(cloud_filter)
    ransac = pcl.RandomSampleConsensus(modle_p)
    ransac.set_DistanceThreshold(threshold)
    ransac.computeModel()
    # ransac.setNegative(True)
    inliers = ransac.get_Inliers()
    # final.extract()
    final = pcl.PointCloud()
    finalpoints = np.zeros((len(inliers), 3), dtype=np.float32)

    for i in range(0, len(inliers)):
                 finalpoints[i][0] = cloud_filter[inliers[i]][0]
                 finalpoints[i][1] = cloud_filter[inliers[i]][1]
                 finalpoints[i][2] = cloud_filter[inliers[i]][2]
    # finalpoints[1][0] = cloud_filter[inliers[1]][0]
    # finalpoints[1][1] = cloud_filter[inliers[1]][1]
    # finalpoints[1][2] = cloud_filter[inliers[1]][2]
    final = pcl.PointCloud()
    final.from_array(finalpoints)
    if ext == True:
        return cloud_filter.extract(inliers, True)
    else:
        return final
def getOBB(cloud, aabb=False):
    x = cloud.make_MomentOfInertiaEstimation()
    x.compute()
    #(max.x, max.y, max.z), (max.x, min.y, max.z), (max.x, max.y, min.z), (min.x, max.y, max.z), (min. x,max.y,min.z),(min.x,min.y,max.z),(min.x,min.y,max.z),(min.x,min.y,min. z)
    if aabb == True:
        min, max = x.get_AABB()
        return min, max
        return np.array([[max[0][0], max[0][1], max[0][2]], [max[0][0], min[0][1], max[0][2]], [max[0][0], max[0][1], min[0][2]], [min[0][0], max[0][1], max[0][2]], [min[0][0], max[0][1], min[0][2]], [min[0][0], min[0][0], max[0][2]], [min[0][0], min[0][1], max[0][2]], [min[0][0], min[0][1], min[0][2]]])
    [min_point_OBB, max_point_OBB, position_OBB, rotational_matrix_OBB] = x.get_OBB()
    ea = sp.DCM2EA(rotational_matrix_OBB)
#    print(rotational_matrix_OBB)
    print('euler: {}'.format(ea))
#    print(min_point_OBB)
    print('position_OBB: {}'.format(position_OBB))
#    p1 = np.array([])
    p1 = rotational_matrix_OBB @ min_point_OBB[0].T + position_OBB
    p2 = rotational_matrix_OBB @ np.array([min_point_OBB[0][0], min_point_OBB[0][1], max_point_OBB[0][2]]).T + position_OBB
    p3 = rotational_matrix_OBB @ np.array([max_point_OBB[0][0], min_point_OBB[0][1], max_point_OBB[0][2]]).T + position_OBB
    p4 = rotational_matrix_OBB @ np.array([max_point_OBB[0][0], min_point_OBB[0][1], min_point_OBB[0][2]]).T + position_OBB
    p5 = rotational_matrix_OBB @ np.array([min_point_OBB[0][0], max_point_OBB[0][1], min_point_OBB[0][2]]).T + position_OBB
    p6 = rotational_matrix_OBB @ np.array([min_point_OBB[0][0], max_point_OBB[0][1], max_point_OBB[0][2]]).T + position_OBB
    p7 = rotational_matrix_OBB @ max_point_OBB[0].T + position_OBB
    p8 = rotational_matrix_OBB @ np.array([max_point_OBB[0][0], max_point_OBB[0][1], min_point_OBB[0][2]]).T + position_OBB
#    print('p1: {}, p2: {}, p3: {}, p4: {}, p5: {}, p6: {}, p7: {}, p8: {}'.format(p1, p2, p3, p4, p5, p6, p7, p8))
#    print(max_point_OBB)
    draw_point = np.array([p1[0], p2[0], p3[0], p4[0], p5[0], p6[0], p7[0], p8[0]])
    # print(draw_point)
    return position_OBB[0], ea[0], draw_point

def get_location(cloud, rangex, rangey, volumel, volumew):
    sor = cloud.make_voxel_grid_filter()
    sor.set_leaf_size(0.1, 0.1, 0.1)

    cloud_filter = sor.filter()
    cloud2 = ModelPlane(cloud_filter)
#     cloud2 = ModelPlane(cloud, True)
    cloud3 = downSample(cloud2, abs(rangex), abs(rangey), 10)
    cloud4, b = do_euclidean_clustering(cloud3)
    if cloud4.size == 0:
        return -1, -1, -1
#    cloud31 = ModelPlane(cloud4, threshold=0.05)
#    points = getOBB(cloud4, True)
    min, max= getOBB(cloud4, True)
    box = cloud.make_cropbox()
    box.set_Translation(0, 0, 0)
    box.set_Rotation(0, 0, 0)
    box.set_MinMax(min[0][1], min[0][1], min[0][2], 0, max[0][0], max[0][1], max[0][2], 10000)
    # box.set_MinMax(-0.329732, -0.399269, -1.985319, 0, 0.549251,  0.279301, -1.505554, 10000)
#    box.set_Min(points[0], points[1], points[2], points[3])
#    box.set_Max(points[4], points[5], points[6], points[7])
    cloud32 = box.filter()
    cloud31 = ModelPlane(cloud32, threshold=0.05)
#     cloud32 = pcl.PointCloud()
    # box.filter(cloud32)
#    cloud5 = ModelPlane(cloud4)
#     pcl.save(cloud4, 'xx1dd.pcd')
    # pcl.save(cloud31, 'xxddd3.pcd')
#    return getOBB(cloud4)
    return getOBB(cloud31)

if __name__ == "__main__":
    cloud = pcl.load('Andre_Agassi_0019.ply')
#    cloud = pcl.load('20201206.pcd')
    cloud2 = pcl.load('xxd.ply')
    get_location(cloud)
#    cloud3 = ModelPlane(cloud2, threshold=0.005 ,ext=True)
#    cloud31 = ModelPlane(cloud2, threshold=0.05)
#    cloud4 = ModelPlane(cloud31, threshold=0.005 ,ext=False)
#    getOBB(cloud31)
#    cloud4 = ModelPlane(cloud3)
#    cloud3 = ModelPlane(cloud2)
    # cloud3 = downSample(cloud2, 2,2,10)
    # cloud4, b = do_euclidean_clustering(cloud3)
    # getOBB(cloud4)

    # cloud4 =
#    pcl.save(cloud3, 'xxddd.pcd')
#    pcl.save(cloud31, 'xxddd2.pcd')