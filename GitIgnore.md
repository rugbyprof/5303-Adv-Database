### Important

Make sure you don't put your usernames and passwords on github! To prevent this we can "ignore" files in our repository. To set that up simply:

1. Create a file called `.gitignore` in your repository folder
2. Add any files you want to ignore inside that file (one per line)
3. You can also add wildcards like `config*`
4. Run the following commands to make sure your `.gitignore` works correctly.

```
git rm -r --cached .
git add .
git commit -m "fixed untracked files"
git push origin master
```
