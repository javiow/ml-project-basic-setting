# My Basic ML Project Environment Settings  
- __W&B(Experiment managing & Hyper Parameter Tuning)__
- __WIT(Model Analysis)__
- __Kubeflow(ML Pipeline)__
    - __How to use kubeflow pipeline on my project__  
    → There are 4 components in this pipeline (data extracting-preprocessing-training-predicting)  
    → __Every components should be uploaded with docker image__    
    → In Shell    
    → ``` cd kubeflow/{component} ```  
    → ``` docker build -t myname/{component_tag_name} . ```  
    → ``` docker login ```  
    → ``` docker push myname/{component_tag_name} ```  
    → ``` cd .. ```  
    → ``` python pipeline.py ``` after all of components uploading  
    → There is a __service which sends email that has an error__
- __CodeClimate(Code Quality Management & Continuous Integration)__
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
        - If you want to stop branch from merging code which has an error __(you have to pay)__ 
            - <span style="color:skyblue">settings - Branches - Branch Protection rules</span>  
            → activate <span style="color:skyblue">Require status checks to pass before merging / Require branches to be up to date before merging</span>  
            → add <span style="color:skyblue">Coverage Report, Lint Code Base</span>  