# 1. Hedonometer: Quantitative and Qualitative Exploration

This group project investigates the **labMT 1.0** “hedonometer” dataset, which attribute happiness scores to words based on ratings from Amazon Mechanical Turk participants. Using data analytic methods, we examine the statistical distribution of word happiness and scores and explore how language can mirror emotional patterns. By grounding quantitative and qualitative ways of exploration of the Hedonometer in our project, we investigate how sentiment is measured and what kind of limitations this dataset may undergo.

## 2. Dataset section
   
  – where it came from
  – what each column means (data dictionary)
  
### Load, Clean, and Describe the dataset  
The dataset was loaded using pd.read_cvs, the tab separation is specified (sep=”/t”) and the first three metadata lines are skipped (skiprows=3). To prevent parsing errors, all columns were read as strings. Replacing -- with just empty space and converting all numeric columns to floating point values for statistical analysis. All words were converted to lowercase to ensure consistency. 
Furthermore, the data set contains 10222 rows and 8 columns. The missing rank value (--) indicates that the word does not appear among the top 5000 most frequent words google, twitter, etc.
  
### Data dictionary (per column)  
   - **word**: A specific word from the dataset. The data type object of this column is a string. No words are missing by default.
   - **happiness_rank**: The rank order of the word based on its average happiness rate. The data type object of this column is a 64-bit float. No happiness ranks were missing, meaning that each word had a happiness rank assigned.
   - **happiness_average**: The average happiness rate based on the ratings given by 50 independent respondents on a scale of 1 to 9. The data type object of this column is a 64-bit float. No average rates were missing, meaning each word had an average happiness rate assigned.
   - **happiness_standard_deviation**: How much raters disagree about the happiness rate. The data type object of this column is a 64-bit float. No standard deviation rates were missing, meaning each word had a standard deviation rate assigned.
   - **twitter_rank**: The rank order of the word based on how many times it showed up in the top 5000 of words in a corpus of Twitter posts. The data type object of this column is a 64-bit float. 5222 words in total were missing from the top 5000 of words in the corpus of Twitter posts.
   - **google_rank**: The rank order of the word based on how many times it showed up in the top 5000 of words in a corpus of Google Books. The data type object of this column is a 64-bit float. 5222 words in total were missing from the top 5000 of words in the corpus of Google Books.
   - **nyt_rank**: The rank order of the word based on how many times it showed up in the top 5000 of words in a corpus of New York Times articles. The data type object of this column is a 64-bit float. 5222 words in total were missing from the top 5000 of words in the corpus of New York Times articles.
   - **lyrics_rank**: The rank order of the word based on how many times it showed up in the top 5000 of words in a corpus of music lyrics. The data type object of this column is a 64-bit float. 5222 words in total were missing from the top 5000 of words in the corpus of music lyrics.

### Sanity Checks  
First, the word column was checked for unique entries, ensuring that no duplicate words appear. This confirms that each word has a single associated happiness score. Second, a random sample of 15 rows was inspected to confirm that the dataset was correctly loaded and cleaned, and that numeric values were converted properly. 

Top 10 most positive and top 10 most negative words based on their average happiness scores were identified. Many positive words align with positive emotions such as love, and joy, while most negative words correspond to concepts associated with suffering, and death. 
In this sense, these words reflect widely shared social understandings of what counts as positive or negative emotion. Emotional meaning is shaped by cultural norms, historical context and perspectives. The strong agreement around words such as ‘suicice”, “rape”, and “murder” suggest that these words show little disagreement, meaning most people agree they are strongly negative. Moreover, they are embedded in moral and legal frameworks that shape how people are expected to evaluate them. It reflects both shared emotional response and what social norms consider harmful and tragic. Thus, the dataset captures a particular social consensus rather than an objective and universal definition of emotion.

## 3. Methods section (what you did in Python)

## 4.  Results section
  – plots + captions
  – interpretation in plain language

## 5. Qualitative “exhibit” of words

## 6. Critical Reflection: How was this dataset generated and why does it matter?

### 6.1 Reconstructing the Pipeline (Data Provenance)

The labMT dataset was created through several steps:
1. **Word selection**: Researchers compiled 10,222 common English words.

2. **Mechanical Turk ratings**: Online workers rated each word on a scale from 1 (sad) to 9 (happy). Multiple ratings per word were averaged to create `happiness_average`.

3. **Calculating disagreement**: For each word, they calculated the standard deviation of ratings (`happiness_standard_deviation`), higher numbers mean more disagreement.

4. **Corpus frequency ranking**: They looked at how often each word appeared in four sources:
   - **Twitter** (social media)
   - **Google Books** (literature)
   - **New York Times** (journalism)
   - **Lyrics** (popular music)

   Words in the top 5,000 of each source got a rank (1 = most common). Words outside the top 5,000 got "--" (missing).

 5. **Final compilation**: The dataset combines happiness scores with frequency information for 10,222 words.

### 6.2 Consequences and Limitations: Five Critical Design Choices
**1: Rating words without context**
- **The choice**: People rated words alone, without sentences.
- **The consequence**: This misses how meaning changes with context. Words with multiple meanings get forced into one score.
- **Example**: "Grand" (7.06, σ=1.3614) can mean "magnificent" (positive) or "a thousand dollars" (neutral). The higher standard deviation (compared to "love" at 1.1082) shows raters disagreed, likely because they imagined different contexts.

**2: Using a simple 1-9 scale**
- **The choice**: Happiness measured as one number from 1-9.
- **The consequence**: This oversimplifies emotions. Fear, anger, and sadness all become just "unhappy."
- **Example**: From your random sample, "suicide" (1.3), "cancer" (1.54), "died" (1.56), and "kill" (1.56) all cluster together despite representing completely different experiences, self-death, disease, loss, and violence. The scale can't tell them apart.

**3: Who did the ratings**
- **The choice**: Ratings came from anonymous MTurk workers, who are mostly U.S.-based, English-speaking, and relatively young.
- **The consequence**: The dataset reflects one demographic's feelings, not universal emotion.
- **Example**: "Naval" (5.48) appears neutral, but might carry specific emotional weight for veterans or military families that the dataset misses. "Lit" (5.64) scores neutral, suggesting raters didn't strongly associate it with its positive slang meaning.

**4: The "top 5000" corpus cutoff**
- **The choice**: Words only ranked if they were among the top 5,000 most frequent in each source.
- **The consequence**: This creates gaps that hide how language differs across domains.
- **Example**: "Prom" (5.94) appears in Twitter (rank 4876) but is missing from Google Books, NYT, and lyrics. This makes sense, people tweet about prom, but it rarely appears in serious writing. But the cutoff means we can't see where "prom" would rank in books (maybe 8,000). "Mis" appears in Twitter and lyrics but not in formal writing, showing how abbreviations live in casual contexts.

**5: A snapshot instead of an ongoing picture**
- **The choice**: The dataset was created at one point in time.
- **The consequence**: Language evolves, new words appear, meanings shift, but the dataset can't capture this.
- **Example**: "Wen" (4.8) appears only in Twitter. Today this might be a misspelling of "when" in texting slang. A 2024 dataset might show different patterns. Words that emerged after the dataset (like "COVID" or "doomscrolling") aren't included at all.

### 6.3 Instrument Note: Using This Dataset Today
**What I would trust this dataset to measure well:**
This dataset reliably captures broad, mainstream emotional associations for common English words as seen by a specific demographic (mostly U.S. English speakers) in the early 2010s. It excels at finding words with strong emotional consensus, your top 10 positives like "laughter" (8.5, σ=0.9313) and "happiness" (8.44, σ=0.9723) show strong agreement, as do your random sample negatives like "suicide" (1.3, σ=0.8391) and "rape" (1.44, σ=0.7866). The extremely low standard deviations here suggest these evaluations are deeply embedded in shared cultural values.
The frequency rankings usefully show how language differs across domains. "On" appears in all four corpora with very high frequency, confirming function words are stable. But "friendship" appears in all four with varying ranks, showing it's universally discussed but more common in books than tweets. "Naval" appears only in Google Books and NYT, a word that belongs to formal discourse.

**What I would NOT claim based on it:**
I would not claim this dataset measures "universal" emotional meaning. The scores can't tell us how words actually make people feel in real life, only how isolated words were rated in an artificial task. I would avoid using it for claims about non-English languages, non-Western cultures, or communities different from the MTurk raters.
The dataset also can't capture emotional nuance. Looking at your random sample, "suicide" (1.3), "cancer" (1.54), "died" (1.56), and "kill" (1.56) all cluster together despite being fundamentally different experiences, grief, fear, loss, violence. The scale treats them as almost the same.
I would also avoid treating missing corpus ranks as evidence that words don't exist in that domain. "Prom" missing from Google Books doesn't mean it never appears in books, just that it's not in the top 5,000. It might be at rank 8,000, but the cutoff hides this.

**How I would improve it:**
First, I would show words in context by presenting them in example sentences, so raters respond to actual usage. This would reduce the "multiple meanings" problem seen with words like "grand" (7.06, σ=1.3614).
Second, I would diversify the rater pool and collect demographic information, allowing analysis of how emotional associations vary by age, region, and background. Words like "prom" (5.94) might mean different things to teenagers versus adults.
Third, I would expand beyond the 1-9 scale by asking raters to select emotion categories (joy, fear, anger, sadness) alongside the happiness score. This would distinguish between different kinds of negative emotions instead of lumping them all as "unhappy."
Fourth, I would include frequency data beyond the top 5,000 and provide percentile ranks instead of arbitrary cutoffs, giving a more complete picture of language distribution.
Finally, I would track changes over time by updating the dataset regularly to capture how word meanings evolve and to include new words (like "COVID") that have emerged since the dataset was created.

## 7. How to run the code

**1: Clone the repository:** In your terminal, type `git clone https://github.com/MommySuperior/Hedonometer`.  
**2: Change directory to the repository:** In your terminal, type `cd Hedonometer`.  
**3: Create a virtual environment:** In your terminal, type `python -m venv .venv` for Windows, or `python3 -m venv .venv` for MacOS.  
**4: Activate virtual environment:** In your terminal, type `.\.venv\Scripts\Activate.ps1` for PowerShell, `.\.venv\Scripts\activate.bat` for Command Prompt, or `source .venv/bin/activate` for MacOS.  
**5: Install requirements.txt:** In your terminal, type `python -m pip install -r requirements.txt` for Windows, or `python3 -m pip install -r requirements.txt` for MacOS.  
**6: Run cleaning.py:** In your terminal, type `python src/cleaning.py` for Windows, or `python3 src/cleaning.py` for MacOS.  
  
## 8. Credits

**Team Roles**
- Repo & workflow lead - Roos
- Data wrangler - Leo
- Quantitative analyst - Razvan
- Qualitative / close-reading lead - Emilis
- Provenance & critique lead - Alessia
- Editor & figure curator - Oskaras

**Citation** (citation for the paper / dataset)
Dodds, Peter Sheridan, Kameron Decker Harris, Isabel M. Kloumann, Catherine A. Bliss, and Christopher M. Danforth. "Temporal patterns of happiness and information in a global social network: Hedonometrics and Twitter." PloS one 6, no. 12 (2011): e26752.

