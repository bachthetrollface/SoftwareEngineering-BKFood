let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");

  if (n > slides.length) {slideIndex = 1}    
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
}

function showSlidess() {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}    
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
  setTimeout(showSlidess, 5000); // Change image every 2 seconds
}

//top dich vu --------------------------------------------------
// openCity(event, 'London')
function openCity(evt, cityName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the link that opened the tab
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}

// Phan comment
const next = document.querySelector('#comment .next')
const prev = document.querySelector('#comment .prev')
const comment = document.querySelector('.post-list')
const commentItem = document.querySelectorAll('.post-list .item')

var translateY = 0
var count = commentItem.length

next.addEventListener('click', function (event) {
event.preventDefault()
if( count == 1){
    translateY += 600*(commentItem.length - 1)
    comment.style.transform = `translateY(${translateY}px`
    count = commentItem.length
}
else{
    translateY += -600
    comment.style.transform = `translateY(${translateY}px`
    count --
}
})

prev.addEventListener('click', function (event) {
    event.preventDefault()
    if( count == commentItem.length){
        translateY += -600*(commentItem.length - 1)
        comment.style.transform = `translateY(${translateY}px`
        count = 1
    }
    else{
        translateY += 600
        comment.style.transform = `translateY(${translateY}px`
        count ++
    }
})


function searchTag(event, tag){
  // reset màu các btnTag
  var btnTags = document.querySelectorAll('.btnTag');
  btnTags.forEach(function(btn) {
      btn.style.backgroundColor = '#fff'; // Thay đổi màu nền thành xám
  });
  // Đổi màu tag hiện tại
  const button = event.currentTarget;
  button.style.backgroundColor = '#fb7';

  var selectElement = document.getElementById("choices");
  var selectedValue = selectElement.value;
  console.log("searchTag", tag);
  var valueTag = tag.replace(/ /g, "_");
  // Gửi yêu cầu AJAX để lấy dữ liệu comment
  $.ajax({
      url: `/homepage/searchTag/${valueTag}/`,
      type: `POST`,
      data: {'choices': selectedValue},
      success: function(response) {
          var containerSearch = document.getElementById("containerSearch");
          containerSearch.innerHTML = '';
          var lengthData;
          if ( selectedValue === 'shop'){
              showShop(response.dataShop, containerSearch);
              lengthData = response.dataShop.length;
          }
          else{
              showProduct(response.dataProduct, containerSearch);
              lengthData = response.dataProduct.length;
          }
          if(lengthData === 0) alert("No results!");
      },
      error: function(error) {
          console.log(error);
      }
  });
}

function showShop(dataShop, containerSearch){
  containerSearch.innerHTML = '';
  dataShop.forEach(function(shop) {
      console.log(shop.id)
      var shopHTML = `
          <div class="post">
              <img class="img-food" src="${shop.avatar}" alt="">
              <div class="info" style="padding-left: 10px;">
                  <div class="text">
                      <h3>${shop.name}</h3>
                      <p>Rating: ${shop.avgStar}/5 <span><img class="search_imgstar" src="{% static 'images/star.png' %}" alt=""></span></p>
                      <p>${shop.district}-${shop.ward}</p>
                  </div>

              </div>
              <hr>
              <div class="cost">
                  <a href="/profile/${shop.id}/">
                      <button>To the diner</button>
                  </a>
              </div>
          </div>
      `;
      containerSearch.innerHTML += shopHTML;
  })
}

function showProduct(dataProduct, containerSearch){
  containerSearch.innerHTML = '';
  dataProduct.forEach(function(product) {
      var productHTML = `
      <div class="post">
          <img class="img-food" src="${product.img}" alt="">
          <div class="info">
              <a href="/profile/${product.provider.id}/"">
                  <img class="img-avt" src="${product.provider.avatar}" alt="">
              </a>
              <div class="text">
                  <h3>${product.name}</h3>
                  <!--<p>Like: {{item.like}}, dislike: {{item.dislike}}</p> -->
                  <p>Provider: ${product.provider.name}</p>

              </div>
          </div>
          <hr>
      </div>
      `;
      containerSearch.innerHTML += productHTML;
  })
}

// Tìm kiếm chính ---------------------
function mainSearch(event){
  var selectElement = document.getElementById("choices");
  var selectedValue = selectElement.value;

  var searchKeyElement = document.getElementById("searchKey");
  var searchKey = searchKeyElement.value;

  var t_openElement = document.getElementById("t_open");
  var t_open = t_openElement.value;
  var t_closedElement = document.getElementById("t_closed");
  var t_closed = t_closedElement.value;

  var cityElement = document.getElementById("city");
  var city = cityElement.value;
  var districtElement = document.getElementById("district");
  var district = districtElement.value;
  var wardElement = document.getElementById("ward");
  var ward = wardElement.value;

  $.ajax({
      url: `/homepage/search/`,
      type: `POST`,
      data: {
          'choices': selectedValue,
          'searchKey': searchKey,
          'city': city, 'district': district, 'ward': ward,
          't_open': t_open,
          't_closed': t_closed,
      },
      success: function(response) {
          var containerSearch = document.getElementById("containerSearch");
          containerSearch.innerHTML = '';
          var lengthData ;
          if ( selectedValue === 'shop'){
              showShop(response.dataShop, containerSearch);
              lengthData = response.dataShop.length;
          }
          else{
              showProduct(response.dataProduct, containerSearch);
              lengthData = response.dataProduct.length;
          }
          if(lengthData === 0) alert("No results!");
      },
      error: function(error) {
          console.log(error);
      }
  });
}