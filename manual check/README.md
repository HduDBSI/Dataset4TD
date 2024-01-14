1. Run [get_positive.py](get_positive.py) to extract all positive samples to directory [Positive](Positive)
2. Run [get_negative.py](get_negative.py) to extract all uncertain negative samples to directory [Negative](Negative)
3. Use [CheckTool](CheckTool) to help annotation.
4. After manual checking, run [updateComment.py](updateComment.py), thereby obtaining `all_comment_checked.csv` and `all_comment_checked_deprecated.csv`
5. Run [update.py](update.py) to update comments' labels, and the checked comments can be found in directory [/comments-with-labels-checked](/comments-with-labels-checked)