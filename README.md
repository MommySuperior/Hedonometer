1.1 Load, Clean, and Describe the dataset
I loaded the dataset using pd.read_cvs, specifying tab separation (sep=”/t”) and skipping the first three metadata lines (skiprows=3). To prevent parsing errors, all columns were read as strings. Replacing -- with just empty space and converting all numeric columns to floating point values for statistical analysis. All words were converted to lowercase to ensure consistency. 
Furthermore, the data set contains 10222 rows and 8 columns. The missing rank value (--) indicates that the word does not appear among the top 5000 most frequent words google, twitter, etc.

1.3 Sanity Checks
I first checked if the word column contains unique entries, ensuring that no duplicate words appear. This confirms that each word has a single associated happiness score. Second, I inspected a random sample of 15 rows to confirm that the dataset was correctly loaded and cleaned, and that numeric values were converted properly. 

Top 10 most positive and top 10 most negative words based on their average happiness scores were identified. Many positive words align with positive emotions such as love, and joy, while most negative words correspond to concepts associated with suffering, and death. 
In this sense, these words reflect widely shared social understandings of what counts as positive or negative emotion. Emotional meaning is shaped by cultural norms, historical context and perspectives. The strong agreement around words such as ‘suicice”, “rape”, and “murder” suggest that these words show little disagreement, meaning most people agree they are strongly negative. Moreover, they are embedded in moral and legal frameworks that shape how people are expected to evaluate them. It reflects both shared emotional response and what social norms consider harmful and tragic. Thus, the dataset captures a particular social consensus rather than an objective and universal definition of emotion.


