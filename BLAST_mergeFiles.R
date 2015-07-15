# this is merge_files function
merge_files <- function (){
  # initialize the dataframe
  df <- data.frame(matrix(vector(), 0, 13, dimnames=list(c(), c("genome","qseqid","sseqid","pident","length","mismatch","gapopen","qstart","qend","sstart","send","evalue","bitscore"))), stringsAsFactors=F)
  # get all files in working directory
  file_list <- list.files()
  for (file in file_list){
    # get the name for extra column
    nombre <- substr(file,41,44)
    # charge the temporal data
    temp_dataset <- read.csv(file, header = FALSE)
    # add extra filled column
    temp_dataset$name <- nombre
    # add to dataframe, erase temporal data
    df<-rbind(df, temp_dataset)
    rm(temp_dataset)
  }
  names(df) <-c("qseqid","sseqid","pident","length","mismatch","gapopen","qstart","qend","sstart","send","evalue","bitscore","genome")
  df
}
