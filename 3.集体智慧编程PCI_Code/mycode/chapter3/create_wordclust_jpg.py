import clusters
blogname,words,data = clusters.readfile('blogdata2.txt')
coords = clusters.scaledown(data)
clusters.draw2d(coords,blogname,jpeg='blog2d.jpg')
rdata = clusters.rotatematrix(data)
wordclust=clusters.hcluster(rdata)
clusters.drawdendrogram(wordclust,labels=words,jpeg='wordclust.jpg')
