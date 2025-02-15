# 3M CLOUD (My Media Management CLOUD)
미디어 파일을 보다 편리하고 손쉽게 관리해주는 클라우드 기반 Dropbox

## 목차
<ol>
<li> 프로젝트 소개 </li> 
<li> 개발 환경 및 기술 스택 </li> 
<li> 서비스 아키텍쳐 </li> 
<li> 구현 기능 </li> 
</ol>

## 프로젝트 소개
사용자의 미디어 파일을 보다 편리하고 손쉽게 제공해줄 수 있는 서비스가 없을까? <br> <br>
<strong> 기존 드롭박스의 기능을 수정해서 업로드 / 다운로드 이외에도 음원 파일 자동 분류, 사진 미리보기, 이미지 용량 줄이기 기능을
갖춘 서비스를 만들어보자! </strong>


## 개발 환경 및 기술 스택
![image](https://user-images.githubusercontent.com/78679830/197355049-5bf658b2-ae31-4684-8d44-4e00b7a0b4b5.png)

## 서비스 아키텍쳐
<img src = "https://user-images.githubusercontent.com/78679830/197355126-488ed55f-8ac8-4dca-a0a0-cc32eb71910a.png" style = "width: 80%; height: 80%;">

## 구현 기능

### 사용자 인증
#### - AWS Cognito 를 사용하였고 회원가입, 로그인, 권한 검증을 처리함.

### 파일 업로드 및 다운로드
#### - AWS S3와 연동하여 파일 업로드 및 다운로드를 처리함.

### 음원 파일 자동 분류
#### - ML을 적용하여 사용자가 파일을 음원 파일을 업로드헀다면 음악 장르 카테고리가 알맞은 폴더에 저장함.

### SVD 분해를 통한 이미지 용량 줄이기 기능
#### - SVD 분해를 사용해서 사용자가 요청한다면 이미지 파일의 압축을 처리함.



