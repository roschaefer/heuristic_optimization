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

plotCurve <- function(Data, xlim=400000, ylim=300) {
	plot(Data$V1, Data$V2, pch = 1, ylim=c(0, ylim), xlim=c(0, xlim), col=rainbow(10)[Data$group],
		ylab="Deviation in %", xlab="Iterations")
}

dirs <- list.dirs("results2")

# for(dir in dirs) {
	dir <- "results2/gr17_RHO-0.100_ALPHA-0.100_BETA-8.000"
	allForParams <- data.frame()
	files <- list.files(dir)
	group <- 0
	plot(1, ylim=c(0, 20000), xlim=c(0,3))

	for(f in files) {
		x <- data.frame()
		x <- read.csv(sprintf("%s/%s", dir,f), header=F)
		colnames(x) <- c("seconds", "V2", "V1")
		x <- x[c("V1", "V2")]
		x$V2<-normalize(x$V2, 2085)
		x$group <- group
		group <- group + 1
		allForParams <- rbind(x, allForParams)
	}
	plotCurve(allForParams)
	means <- meanOfBins(allForParams)$Means
	lines(means$V1, means$V2, lwd=2, type="l", col="black")
	# draw axis showing buckets
	axis(3, means$V1, labels=F)


# }