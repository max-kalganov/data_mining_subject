library(ggplot2)
data_matrix <- cbind(c(rnorm(40, mean = 1, sd = 1),
                       rnorm(40, mean = 10, sd = 1)),
                     c(rnorm(40, mean = 1, sd = 1),
                       rnorm(40, mean = 10, sd = 1)),
                     rep(1, 80),
                     rep(1, 80))
colnames(data_matrix) <- c("x", "y", "col", "size")

centroids_ids = sample(1:80, 2)

c1 <- data_matrix[centroids_ids[1], 1:2]
c2 <- data_matrix[centroids_ids[2], 1:2]

data_matrix[centroids_ids[1], 3] <- 2
data_matrix[centroids_ids[2], 3] <- 3
data_matrix[centroids_ids[1], 4] <- data_matrix[centroids_ids[2], 4] <- 3

plot(data_matrix, col=data_matrix[, 3], pch=19, cex=data_matrix[, 4])

diff_c1 <- sweep(data_matrix[, 1:2], 2, c1) 
diff_c2 <- sweep(data_matrix[, 1:2], 2, c2) 

dist_c1 <- rowSums(diff_c1 ^ 2)
dist_c2 <- rowSums(diff_c2 ^ 2)

data_matrix[, 3] <- ifelse(dist_c1 < dist_c2, 2, 3)
