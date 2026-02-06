<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>CV Generator | Özgeçmiş Oluşturucu</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.9.2/html2pdf.bundle.min.js"></script>

<style>
body {
  font-family: 'Poppins', sans-serif;
  background: #f2f4f8;
  margin: 0;
}

header {
  background: linear-gradient(90deg, #5f2cff, #3fa9f5);
  color: white;
  padding: 20px;
  text-align: center;
}

.container {
  display: flex;
  padding: 20px;
}

.form {
  width: 40%;
  background: white;
  padding: 20px;
  border-radius: 10px;
  margin-right: 20px;
  overflow-y: auto;
  height: 85vh;
}

.preview {
  width: 60%;
  background: white;
  padding: 20px;
  border-radius: 10px;
}

input, textarea, select {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

button {
  background: #5f2cff;
  color: white;
  padding: 12px;
  border: none;
  width: 100%;
  border-radius: 5px;
  cursor: pointer;
}

.cv {
  padding: 20px;
  border-left: 8px solid var(--theme);
}

.photo {
  width: 120px;
  height: 120px;
  border-radius: 100%;
  object-fit: cover;
}

h1, h2 {
  color: var(--theme);
}
</style>
</head>

<body>
<header>
  <h1>CV Generator | Özgeçmiş Oluşturucu</h1>
</header>

<div class="container">

<div class="form">
<select id="lang">
  <option value="tr">Türkçe</option>
  <option value="en">English</option>
</select>

<input type="color" id="theme" value="#5f2cff">

<input placeholder="Ad / Name" id="name">
<input placeholder="Soyad / Surname" id="surname">
<input placeholder="Ülke / Country" id="country">
<input placeholder="Şehir / City" id="city">
<input placeholder="Telefon / Phone" id="phone">
<input placeholder="E-mail" id="email">

<textarea placeholder="Profesyonel Özet / Professional Summary" id="summary"></textarea>
<textarea placeholder="İş Deneyimi / Work Experience" id="experience"></textarea>
<textarea placeholder="Eğitim / Education" id="education"></textarea>
<textarea placeholder="Yetenekler / Skills" id="skills"></textarea>
<textarea placeholder="Sertifikalar / Certificates" id="certificates"></textarea>

<input type="file" id="photo">

<button onclick="generate()">CV Oluştur</button>
<button onclick="downloadPDF()">PDF İndir</button>
</div>

<div class="preview">
<div class="cv" id="cv">
<img id="img" class="photo"><br>
<h1 id="cvname"></h1>
<p id="location"></p>
<p id="contact"></p>

<h2 id="t1"></h2>
<p id="cvsummary"></p>

<h2 id="t2"></h2>
<p id="cvexp"></p>

<h2 id="t3"></h2>
<p id="cvedu"></p>

<h2 id="t4"></h2>
<p id="cvskills"></p>

<h2 id="t5"></h2>
<p id="cvcert"></p>
</div>
</div>

</div>

<script>
function generate(){
 let lang = document.getElementById("lang").value;
 let theme = document.getElementById("theme").value;
 document.getElementById("cv").style.setProperty("--theme", theme);

 let name = document.getElementById("name").value;
 let surname = document.getElementById("surname").value;
 let country = document.getElementById("country").value;
 let city = document.getElementById("city").value;
 let phone = document.getElementById("phone").value;
 let email = document.getElementById("email").value;

 document.getElementById("cvname").innerText = name + " " + surname;
 document.getElementById("location").innerText = country + " / " + city;
 document.getElementById("contact").innerText = phone + " | " + email;

 document.getElementById("cvsummary").innerText = summary.value;
 document.getElementById("cvexp").innerText = experience.value;
 document.getElementById("cvedu").innerText = education.value;
 document.getElementById("cvskills").innerText = skills.value;
 document.getElementById("cvcert").innerText = certificates.value;

 if(lang=="tr"){
  t1.innerText="Profesyonel Özet";
  t2.innerText="İş Deneyimi";
  t3.innerText="Eğitim";
  t4.innerText="Yetenekler";
  t5.innerText="Sertifikalar";
 } else {
  t1.innerText="Professional Summary";
  t2.innerText="Work Experience";
  t3.innerText="Education";
  t4.innerText="Skills";
  t5.innerText="Certificates";
 }

 let file = document.getElementById("photo").files[0];
 let reader = new FileReader();
 reader.onload = e => img.src = e.target.result;
 if(file) reader.readAsDataURL(file);
}

function downloadPDF(){
 html2pdf(document.getElementById("cv"));
}
</script>

</body>
</html>
