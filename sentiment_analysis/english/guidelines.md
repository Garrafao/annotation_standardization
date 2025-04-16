# Sentiment Annotation
In the Sentiment Annotation task, annotators are shown a single text and are asked to rate the emotional sentiment as "positive", "neutral", and "negative". These are denoted by the labels (2,1,0) accordingly. The non-label "-" is used when the annotator is unable to make a judgment.

For example, consider the following text:

| Text                                                | Label |
|--------------------------------------------------------|-------------|
|"Amazon prime is literally a lie....I ordered a book LAST MONDAY; it still isn't here. do better". | 0 |

Here the label is 0 because the sentiment of the text is negative. When assessing items, the annotator should take into account the posibility that a text is sarcastic. The following text would also be assessed as negative:

| Text                                                | Label |
|--------------------------------------------------------|-------------|
|"Thanks manager for putting me on the schedule for Sunday". | 0 |

The annotator must consider the knowledge that working on a Sunday is generally unpopular to infer that the writer is being sarcastic.

In the next example, we see a text that would be assessed as neutral.

| Text                                                | Label |
|--------------------------------------------------------|-------------|
|"Ryan Braun returned to the lineup on Wednesday after missing two games with lower back tightness."| 1 |

This example is assigned a neutral label because the text does not contain a negative or positive emotional sentiment. Texts that are statements of facts or neutra questions should receive this label.

Finally, the annotator will label sentences as positive that contain a strong positive emotional sentiment. Consider the following example:

| Text                                                | Label |
|--------------------------------------------------------|-------------|
|"Another great night in Split, off to Hvar on the 8:30 ferry tomorrow morning... dreading the packing but excited to get there!" | 2 |