# Hadoop MapReduce Lab – AWS EMR

**GitHub Repository:** [emr-mapreduce-lab](https://github.com/mohamadjabaren/emr-mapreduce-lab/tree/main/emr-mapreduce-lab)

---

## Exercise 1

### Q1. How many files are there?
There are **6** data partition files (`part-00000` to `part-00005`) plus **1** `_SUCCESS` status file (**7** items in total in `/user/hduser/gutenberg-output`).

### Q2. Did the number of mappers change?
The number of input splits remained **9**, while `Launched map tasks` changed from **9** to **10** because 1 map task was killed (`Killed map tasks=1`) and re-launched as an extra attempt.

### Q3. Did the number of reducers change?
**Yes**, it changed from **3** to **6** after passing `-numReduceTasks 6`.

### Q4. Did the number of output files change? Why?
**Yes**, the number of data output files increased from **3** to **6**. Each reduce task writes its own partition output file (`part-xxxxx`), so increasing the number of reducers from 3 to 6 produced 6 data output files (alongside the `_SUCCESS` file).

### Q5. What does the value of 'Merged Map outputs' represent, and how is it calculated?
It represents the total number of map output partitions fetched and merged across all reducers during the shuffle and merge phase. It is calculated as:

$$\text{Merged Map outputs} = \text{Number of Map Splits} \times \text{Number of Reduce Tasks}$$

* **First run (3 reducers):** $9 \times 3 = 27$
* **Second run (6 reducers):** $9 \times 6 = 54$

---

## Exercise 2

### Q1. Is your change in the mapper or in the reducer?
The change is in the **mapper** (`mapper.py`), where trailing commas and periods are stripped (`.rstrip('.,')`) and all words are converted to lowercase (`.lower()`) before emitting `(word, 1)` pairs.

### Q2. Please provide your code on GitHub
* **File link:** [`mapper.py`](https://github.com/mohamadjabaren/emr-mapreduce-lab/blob/main/emr-mapreduce-lab/mapper.py)

```python
#!/usr/bin/env python
"""mapper.py"""
import sys


def read_input(file):
    for line in file:
        yield line.split()


def main(separator='\t'):
    data = read_input(sys.stdin)
    for words in data:
        for word in words:
            cleaned_word = word.rstrip('.,').lower()
            if cleaned_word:
                print('%s%s%d' % (cleaned_word, separator, 1))


if __name__ == "__main__":
    main()
```

---

## Exercise 3

### Q1. Is your change in the mapper or in the reducer?
The change is in the **reducer** (`reducer.py`), which aggregates word counts, sorts them in descending order by frequency inside Python, and outputs only the top 3 results (run with `-numReduceTasks 1` to ensure a single global top-3 output).

### Q2. Please provide your code on GitHub
* **File link:** [`reducer.py`](https://github.com/mohamadjabaren/emr-mapreduce-lab/blob/main/emr-mapreduce-lab/reducer.py)

```python
#!/usr/bin/env python
"""reducer.py"""
from itertools import groupby
from operator import itemgetter
import sys


def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)


def main(separator='\t'):
    data = read_mapper_output(sys.stdin, separator=separator)
    word_counts = []
    for current_word, group in groupby(data, itemgetter(0)):
        try:
            total_count = sum(int(count) for current_word, count in group)
            word_counts.append((current_word, total_count))
        except ValueError:
            pass
    word_counts.sort(key=lambda x: x[1], reverse=True)
    for word, count in word_counts[:3]:
        print("%s%s%d" % (word, separator, count))


if __name__ == "__main__":
    main()
```

### Q3. Print the output of the MapReduce and put in your GitHub as an image

```text
the	74369
and	42768
of	34588
```

![MapReduce Top 3 Output](Screenshot%202026-11-20%20154144.png)
