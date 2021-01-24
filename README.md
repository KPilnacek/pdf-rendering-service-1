# PDF Rendering Service

## Project setup

### 1. Start service
To start the API service, run the following command:
```
make start-dev
```

### 2. Migrate DB

```
make migrate-db
```

### 3. Enjoy!

## Using the service

## 1. Upload PDF file

```
curl \
  -H 'Content-Disposition: attachment; filename=document.pdf' --data-binary @path/to/a/document.pdf \
  'http://localhost:8000/documents'
```

## 2. Get status info about document processing
```
curl http://localhost:8000/documents/1
```

## 3. Fetch individual PNG pages with:
```
curl http://localhost:8000/documents/1/pages/1 -o ~/Downloads/page.png
```

## Project update

### 1. Update backend

```
git pull
```

### Update DB schema

run DB forward migration:
```
make migrate-db
```


## Other usages
see in MakeFile
