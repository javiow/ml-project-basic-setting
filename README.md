# My Basic ML Project Environment Settings  
- W&B(Experiment managing & Hyper Parameter Tuning)
- WIT(Model Analysis)
- Kubeflow(ML Pipeline)
- CodeClimate(Code Quality Management & Continuous Integration)
    - __How to apply codeclimate's service on my project__  
    → [CodeClimate](https://codeclimate.com/)  
    → Login  
    → Quality  
    → Github connect  
    → Create a new repository  
    → Add a repo  
    → click the repo  
        - Activate <span style="color:skyblue">Repo setting - Github - Summary comments</span> (comments code reviews)  
        - Activate <span style="color:skyblue">Repo setting - Github - Pull request status updates + Webook on Github</span> (auto-static analysis)  
        - copy token in <span style="color:skyblue">repo setting - test coverage</span>  
        → paste the token in ```.github/workflow/coverage.yml: CODECLIMATE_REPO_TOKEN: { }```  
    → Code commits  
    → You can see where an error comes up in <span style="color:skyblue">Github repository - pull requests</span>  
        - If you want to stop branch from merging code which has an error<span style="color:orange"> __(you have to pay)__ </span>
            - <span style="color:skyblue">settings - Branches - Branch Protection rules</span>  
            → activate <span style="color:skyblue">Require status checks to pass before merging / Require branches to be up to date before merging</span>  
            → add <span style="color:skyblue">Coverage Report, Lint Code Base</span>  