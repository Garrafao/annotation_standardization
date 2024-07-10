# Usage Rank Annotation Task
In the Usage Rank (URANK) annotation task, the annotators are asked to rank a set of sentences with a target word according to a specified criterion. The number of sentences may vary based on the task and annotation requirements. For example, the property could be something like ambiguity, abstractness, sentiment, or emotional valence. For the sake of illustration, the criterion for this tutorial will be **abstractness**.

In this task you will view pairs of sentences containing the target word. Depending on the nature of the experiment, the set of sentences can be of any length. However, for the purpose of demonstration, we will consider the ranking of sentence pairs. You will rank the sentences based on the level of abstractness contained in the sentences. A higher rank (1) correpsonds to high abstractness, and the lower rank (2) corresponds to low abstractness. If you find you are unable to assess the sentence pairs, you may use the non-label (-). For example, the following example contains two uses of the word **scholarship**:

| Context                                                | Target Word |
|--------------------------------------------------------|-------------|
| John was offered a **scholarship** to study at a prestigious university. | scholarship |
| The level of **scholarship** has been steadily declining at the university. | scholarship |

As the annotator, you must now assign a value of 1, 2, or non-label (-) to each sentence. In this case, the second sentence would receive the label "1" because the concept of scholarship in the sense of academic work is more abstract than the meaning of scholarship as a monetary award for academic performance. Consequently, the annotator should assign the label "2" to the first sentence as the meaning of the target is less abstract.

To further illustrate the point, consider the word **record** in the following sentence pair:

| Context                                                | Target Word |
|--------------------------------------------------------|-------------|
| The band has been busy working on their next **record**. | reecord |
| The radio dj is always careful to catalogue her **records** by genre.| record |

The first sentence referse to a **record** in an abstract sense as a work of art. In the case of the second sentence, the target word refers to a physical product and should receive the label "1". Therefore, the annotator should assign the label "2" because the phsyical is less abstract than the **record** as a musical composition.

The non-label may be used in cases where the annotator is unable to make an assessment. This could be for any number of reasons, from unfamiliarity with the context to inability to rank the pair with confidence. For example, let's take these two uses of the target word **tree**.

| Context                                                | Target Word |
|--------------------------------------------------------|-------------|
| We sat by the old oak **tree** and discussed our plans. | tree |
| The spruce **tree** in our garden will need to be trimmed soon.| tree |

In both contexts, the target word refers to a concrete **tree** and it is therefore impossible to determine which is more abstract. Therefore we would assign the label "-" to both sentences.

Likewise, if we take into account this next sentence pair with tree, we can see that it is impossible to appropriately assign a label:

| Context                                                | Target Word |
|--------------------------------------------------------|-------------|
| Look at the **tree**. | tree |
| The spruce **tree** in our garden will need to be trimmed soon.| tree |

Here, the second sentence refers to a concrete tree. However, the first sentence is more ambiguous. The object could be a tree in a concrete sense, but it could also be some abstract concept such as a "family tree" or a representation like a "tree graph". Because of this ambiguity, we would assign both uses a non-lable (-).