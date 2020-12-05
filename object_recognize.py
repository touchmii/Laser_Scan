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
    # ec.set_MaxClusterSize(60000)
    ec.set_MinClusterSize(100)
    ec.set_MaxClusterSize(600)
    ec.set_SearchMethod(tree)
    cluster_indices = ec.Extract()
    # cluster_color = get_color_list(len(cluster_indices))
    color_cluster_point_list = []
    # for j, indices in enumerate(cluster_indices):
    for indice in cluster_indices[0]:
        # for i, indice in enumerate(indices):
        #     color_cluster_point_list.append([white_cloud[indice][0], white_cloud[indice][1], white_cloud[indice][2], rgb_to_float(cluster_color[j])])
        color_cluster_point_list.append([white_cloud[indice][0], white_cloud[indice][1], white_cloud[indice][2]])
    cluster_cloud = pcl.PointCloud()
    cluster_cloud.from_list(color_cluster_point_list)
    return cluster_cloud,cluster_indices

def ModelPlane(cloud_filter):
    modle_p = pcl.SampleConsensusModelPlane(cloud_filter)
    ransac = pcl.RandomSampleConsensus(modle_p)
    ransac.set_DistanceThreshold(0.1)
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
    return cloud_filter.extract(inliers, True)
def getOBB(cloud):
    x = cloud.make_MomentOfInertiaEstimation()
    x.compute()
    [min_point_OBB, max_point_OBB, position_OBB, rotational_matrix_OBB] = x.get_OBB()
    ea = sp.DCM2EA(rotational_matrix_OBB)
    print(rotational_matrix_OBB)
    print(ea)
    print(min_point_OBB)
    print(position_OBB)
    print(max_point_OBB)
    return position_OBB

def get_location(cloud):
    sor = cloud.make_voxel_grid_filter()
    sor.set_leaf_size(0.1, 0.1, 0.1)

    cloud_filter = sor.filter()
    cloud2 = ModelPlane(cloud_filter)
    cloud3 = downSample(cloud2, 2, 2, 10)
    cloud4, b = do_euclidean_clustering(cloud3)
    return getOBB(cloud4)

if __name__ == "__main__":
    cloud = pcl.load('Andre_Agassi_0019.ply')
    location(cloud)
    # cloud2 = ModelPlane(cloud)
    # cloud3 = downSample(cloud2, 2,2,10)
    # cloud4, b = do_euclidean_clustering(cloud3)
    # getOBB(cloud4)

    # cloud4 =
    # pcl.save(cloud4, 'xxd.ply')