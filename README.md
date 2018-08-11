# 원광대학교 졸업 정보 서비스

원광대학교 인트라넷 데이터를 크롤링해 졸업 관련 정보를 제공하는 웹 서비스 입니다.

## 제공 정보

- 사용자 정보
  - 이수과목 정보
  - 전공과목 정보
  - 교양과목 정보
- 학점 현황
- 성적 현황
- 장학금 현황
- WPOINT

## 사용 기술

- Python
- Django
- Selenium
- Beautifulsoup4
- Postgresql
- AWS EC2
- Nginx
- Uwsgi

---------------------------------------------

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

### 디렉토리 이동

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

### 개발환경 실행

- 실제 DB에 테이블을 생성하기 위해 **Migration**을 DB에 적용합니다

~~~shell
$ python manage.py migrate
~~~

- 이제 **Django**서버를 실행시켜줍니다

~~~shell
$ python manage.py runserver 
~~~

---------------------------------------------

### 개발환경 설정

- 프로젝트를 실행하기전에 **intranet.py** 와 **settings.py** 부분을 수정해줘야합니다

---

### settings.py 설정

- 프로젝트를 열어 **intra_crawling** 디렉토리에 있는 **settings.py** 열어 이미지파일처럼 수정해줍니다

![aa](https://user-images.githubusercontent.com/37236133/43987612-380bddbc-9d5e-11e8-9018-d5a9dd6e9928.jpeg)

---

### intranet.py 설정

1. 먼저 **ChromeDriver**를 설치하기 위해 아래 주소를 통해서 들어간다

   [ChromeDriver 다운](https://sites.google.com/a/chromium.org/chromedriver/downloads)

2. 버전을 클릭하면 **OS**별 **Driver**파일이 나타난다 사용하는 **OS**에 맞는 **Driver**를 다운받습니다
   ![d](https://user-images.githubusercontent.com/37236133/43987713-1e238538-9d60-11e8-803c-ee3d87ede3a5.jpeg)

3. **Zip** 파일을 받고 압축해제를 하면 **chromedriver**라는 파일이 저장됩니다

4. 아래 폴더를 기준으로 할 경우 **/Users/marine/Downloads/chromedriver** 가 Driver의 위치입니다 
   **꼭! 기억해주세요** (***PC마다 위치는 다를수있습니다***)

   ![c](https://user-images.githubusercontent.com/37236133/43987617-50c0ffcc-9d5e-11e8-8f08-821826c734df.jpeg)

5. 이제 **webcrawler** 디렉토리에 있는 **intranet.py** 열어 아래에 있는 이미지파일처럼 수정해줍니다
   (**각자 다운받은 위치에 있는 주소를 넣어주셔야합니다**)

![bb](https://user-images.githubusercontent.com/37236133/43987620-5970cc38-9d5e-11e8-9dbe-c00472cd24ad.jpeg)

---

