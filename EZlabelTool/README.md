Please visit our website from uni of Adelaide campus or by VPN off campus : http://10.90.185.16:3000/#/signin

The main working directories and files of EZlabel are listed below:

```markdown
├── back-end
│   ├── app.py
│   ├── controller                *this folder contains service handles*
│   │   ├── Dataset.py
│   │   ├── Editor.py
│   │   ├── Label.py
│   │   ├── Label_info.py
│   │   ├── Member.py
│   │   ├── Project.py
│   │   ├── Task.py
│   │   ├── User.py
│   │   └── Util.py
│   └── model :                  *this foler contains databases operations*
│       ├── DatasetDB.py
│       ├── EditorDB.py
│       ├── LabelDB.py
│       ├── Label_infoDB.py
│       ├── MemberDB.py
│       ├── ProjectDB.py
│       ├── TaskDB.py
│       └── UserDB.py
│   
└── front-end
    └── src                      *this is our working folder*
        ├── Router.js            *this is for setting page access path*
        ├── Utils
        │   ├── ApiUtil.js       *Api to back-end*
        │   └── HttpUtil.js      *packaging two method:post and get*
        ├── pages
        │   ├── Dataset.js       *this and the following are for dataset module*
        │   ├── DatasetGetImages.js
        │   ├── DatasetInfoDialog.js
        │   ├── DatasetUploadDialog.js
        │   ├── Editor.js        *this and the following are for editor module*
        │   ├── EditorChoose.js
        │   ├── EditorInfoDialog.js
        │   ├── EditorSetting.js
        │   ├── FramePage.js     *this and the next are for home page operations*
        │   ├── FrameChangePassword.js     
        │   ├── Import.js        *this is for import reference module*
        │   ├── Label.js         *this and the following are for labelling module*
        │   ├── LabelView.js 
        │   ├── ImageFromUrl.js
        │   ├── Annotation.js
        │   ├── Project.js       *this and the following are for project module*
        │   ├── ProjectDetail.js
        │   ├── ProjectInfoDialog.js
        │   ├── ProjectSetting.js
        │   ├── ProjectSettingEditor.js
        │   ├── ProjectSettingEditorSetting.js
        │   ├── ProjectSettingPermission.js
        │   ├── ProjectSettingRole.js
        │   ├── Review.js       *this and the following are for review process in label module*
        │   ├── ReviewView.js
        │   ├── Signin.js        *this is for signin module*
        │   └── User.js          *this is for user module*
        └── serviceWorker.js


```



How to use our project:

docker for front-end develop：

```
cd front-end/
docker build -t team1-front-end:v{vision} .
```

for test:

```
docker run -it --rm -p 3000:3000 team1-front-end:v{vision}
```

deploy it:

```
docker run -d -p 3000:3000 --name team1-front-end-deploy team1-front-end:v{vision}
```

Open localhost:3000 on your computer



docker for back-end develop:

```
docker build -t team1-back-end:v{vision} .
```

for test:

```
docker run -it --rm -p 5000:5000 team1-back-end:v{vision}
```

deploy it:

```
docker run -d -p 5000:5000 --name team1-back-end-deploy team1-back-end:v{vision}
```

Open localhost:5000 on your computer

Files that required change before deploy to the server:
```
/front-end/package.json
/front-end/ApiUtil.js
/back-end/app.py
/back-end/controller/Task.py
```

