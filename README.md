# 전체 설치 과정 

```shell
$ git clone https://github.com/min-ki/WGP.git
$ cd WGP
$ git remote add wgp_repo https://github.com/min-ki/WGP.git
$ pip install pipenv
$ pipenv --three
$ pipenv install -r requirements.txt
$ pipenv shell
$ python manage.py migrate
$ python manage.py runserver 
```

-------------------------

### 프로젝트 생성

- 프로젝트 폴더를 하나 만들고 터미널을 열어 **프로젝트**를 생성합니다

```shell
$ git clone https://github.com/min-ki/WGP.git
```

-----------------------------------------

###디렉토리 이동

- **WGP** 디렉토리 이동

~~~ shell
$ cd WGP
~~~

------------------------------------------

### 저장소 지정

- **로컬**과 **원격 저장소**를 연결합니다

~~~ shell
$ git remote add wgp_repo https://github.com/min-ki/WGP.git
~~~

-------------------------

### 작업 환경 설치

1. **pip**를 이용하여 [Pipenv](http://docs.pipenv.org/en/latest/)를 설치한다

```shell
$ pip install pipenv
```

2. **python** 버젼은 **3**로 지정해줍니다

~~~shell
$ pipenv --three
~~~

3. **requirements.txt** 에 패키지 리스트를 저장하여 다른 작업환경에서 개발환경을 동일하게 유지하게 합니다

~~~shell
$ pipenv install -r requirements.txt
~~~

4. 패키지를 설치후 **가상환경**을 만듭니다

~~~shell
$ pipenv shell
~~~

------------------------------------------

### 개발환경 실행###

- 실제 DB에 테이블을 생성하기 위해 **Migration**을 DB에 적용합니다

~~~shell
$ python manage.py migrate
~~~

- 이제 **Django**서버를 실행시켜줍니다

~~~shell
$ python manage.py runserver 
~~~

---------------------------------------------

