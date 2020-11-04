//$(document).ready(function() {
//    $('#brand_name').change(function() {
//
//      var brand_name = $('#brand_name').val();
//
//      // Make Ajax Request and expect JSON-encoded data
//      $.getJSON(
//        '/get_product' + '/' + brand_name,
//        function(data) {
//
//          // Remove old options
//          $('#product_name').find('option').remove();
//
//          // Add new items
//          $.each(data, function(key, val) {
//            var option_item = '<option value="' + val + '">' + val + '</option>'
//            $('#product_name').append(option_item);
//          });
//        }
//      );
//    });
//    $("#addMore").click(function(e) {
//        e.preventDefault();
//        $("#fieldList").append("<div class='field is-horizontal'>
//          <div class='field-label is-normal'>
//            <label class='label'>Brand</label>
//          </div>
//          <div class='field-body'>
//            <div class='field'>
//              <div class='control'>
//                    <input class='input' type='text' name='productprofit'>
//              </div>
//            </div>
//          </div>
//        </div>");
//      });
//    });
//  });
//
//  $(function() {
//  $("#addMore").click(function(e) {
//    e.preventDefault();
//    $("#fieldList").append("<div class='field is-horizontal'>
//      <div class='field-label is-normal'>
//        <label class='label'>Brand</label>
//      </div>
//      <div class='field-body'>
//        <div class='field'>
//          <div class='control'>
//                <input class='input' type='text' name='productprofit'>
//          </div>
//        </div>
//      </div>
//    </div>");
//  });
//});
        $("#addMore").click(function(e) {
            e.preventDefault();
            $("#areaproduct").append("<p>coba</p>");
          });


//    $(document).ready(function() {
//        $('#brand_name').change(function() {
//
//          var brand_name = $('#brand_name').val();
//
//          // Make Ajax Request and expect JSON-encoded data
//          $.getJSON(
//            '/get_product' + '/' + brand_name,
//            function(data) {
//
//              // Remove old options
//              $('#product_name').find('option').remove();
//
//              // Add new items
//              $.each(data, function(key, val) {
//                var option_item = '<option value="' + val + '">' + val + '</option>'
//                $('#product_name').append(option_item);
//              });
//            }
//          );
//        });
//        $("#addMore").click(function(e) {
//            e.preventDefault();
//            $("#productform").append("<div class='field is-horizontal'><div class='field-label is-normal'> <label class='label'>Brand</label></div><div class='field-body'><div class='field'><div class='control'><input class='input' type='text' name='productprofit'></div></div></div></div>");
//          });
//        });
//      });