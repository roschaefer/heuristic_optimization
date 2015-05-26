meanOfBins <- function(Data, xlim=NULL, nBins=10, ylim=3) {
	Data.sort <- Data#[order(Data$V1),]

	Means <- data.frame(V1=NaN, V2=NaN)
	if(is.null(xlim)) {
		xlim <- max(Data.sort$V1)
	}
	lowerLimit <- 0
	upperLimit <- xlim/nBins
	step <- floor(upperLimit)
	for(i in 1:nBins){
		V1 <- mean(c(lowerLimit, upperLimit))
		V2 <- mean(subset(Data.sort, Data.sort$V1 >= lowerLimit & Data.sort$V1 < upperLimit)$V2)
		if(is.nan(V2)) {
			stopifnot(i != 0)
			V2 <- Means[i-1,]$V2 # use predecessor
		}
		Means[i,] <- c(V1, V2)
		# todo add point for beginning and end of bin
		lowerLimit <- upperLimit
		upperLimit <- lowerLimit + step

	}
	return(list(Means=Means, Data.sort=Data.sort))
}

normalize <- function(y, optimum) {
	# percentage of deviation
	y <-  100 * y / optimum - 100
}

plotCurve <- function(Data, xlim=500000, ylim=250) {
	plot(Data$V1, Data$V2, pch = 1, ylim=c(0, ylim), xlim=c(0, xlim), col=rainbow(10)[Data$group],
		ylab="Deviation in %", xlab="Iterations")
}

ROOT_DIR <- "results2"
dirs <- list.dirs(ROOT_DIR)

for(d in 2:length(dirs)) {
	dir <- dirs[d]
	if(grepl("fri26", dir)) {
		optimum <- 937
	}
	else if (grepl("gr17", dir)) {
		optimum <- 2085
	}
	pdf(sprintf("%s/plot.pdf", dir))
	allForParams <- data.frame()
	files <- list.files(dir, pattern="*.txt")
	group <- 0
	for(f in files) {
		x <- read.csv(sprintf("%s/%s", dir,f), header=F)
		x <- data.frame(V1=x$V3, V2=x$V2)
		x$V2<-normalize(x$V2, optimum)
		x$group <- group
		group <- group + 1
		allForParams <- rbind(x, allForParams)
	}
	plotCurve(allForParams)
	means <- meanOfBins(allForParams)$Means
	lines(means$V1, means$V2, lwd=2, type="l", col="black")
	# draw axis showing buckets
	axis(3, means$V1, labels=F)
	dev.off()


}