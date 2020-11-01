library(ggplot2)

clusterize <- function(matr, clusters){
  diff_c1 <- sweep(matr[, 1:2], 2, clusters[1]) 
  diff_c2 <- sweep(matr[, 1:2], 2, clusters[2]) 
  
  dist_c1 <- rowSums(diff_c1 ^ 2)
  dist_c2 <- rowSums(diff_c2 ^ 2)
  
  matr[, 3] <- ifelse(dist_c1 < dist_c2, 2, 3)
  return(matr)
}

get_new_clusters <- function(matr){
  cluster1 <- subset(matr, matr[, 3] == 2)
  cluster2 <- subset(matr, matr[, 3] == 3)
  
  new_cluster1 <- colMeans(cluster1)[1:2]
  new_cluster2 <- colMeans(cluster2)[1:2]
  
  return(rbind(new_cluster1, new_cluster2))
}

init_clusters <- function(matr){
  centroids_ids = sample(1:80, 2)
  
  c1 <- data_matrix[centroids_ids[1], 1:2]
  c2 <- data_matrix[centroids_ids[2], 1:2]
  return(rbind(c1, c2))
}



data_matrix <- cbind(c(rnorm(40, mean = 1, sd = 1),
                       rnorm(40, mean = 10, sd = 1)),
                     c(rnorm(40, mean = 1, sd = 1),
                       rnorm(40, mean = 10, sd = 1)),
                     rep(1, 80))
colnames(data_matrix) <- c("x", "y", "col")

plot(data_matrix, col=data_matrix[, 3], pch=19)

clusters <- init_clusters(data_matrix)
data_matrix <- clusterize(data_matrix, clusters)
new_clusters <- get_new_clusters(data_matrix)
plot(data_matrix, col=data_matrix[, 3], pch=19)


while (any(clusters != new_clusters)){
  clusters = new_clusters
  data_matrix <- clusterize(data_matrix, clusters)
  new_clusters <- get_new_clusters(data_matrix)
}

plot(data_matrix, col=data_matrix[, 3], pch=19)


