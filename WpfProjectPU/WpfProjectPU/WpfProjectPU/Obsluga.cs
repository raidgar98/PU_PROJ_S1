using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using System.Diagnostics;
using System.Net;
using System.IO;

namespace WpfProjectPU
{
    public class Obsluga
    {
        string url=@"http://79.175.220.50:8090";
        
        public Obsluga() {
            
        }

        public jsonRPCResult<Dictionary<string, int>> getBrands()
        {
            var date = Newtonsoft.Json.JsonConvert.SerializeObject(new jsonRPCRequest {method= "cars.brands", _params= new Dictionary<string, int>() });
            var encodedData = Encoding.ASCII.GetBytes(date);
            var request = (HttpWebRequest)WebRequest.Create(url);
            request.ContentType = "application/json";
            request.ContentLength = encodedData.Length;
            request.Method = "POST";

            using (var stream = request.GetRequestStream())
            {
                stream.Write(encodedData, 0, encodedData.Length);
            }

            var response = (HttpWebResponse)request.GetResponse();
            
            var responseString = new StreamReader(response.GetResponseStream()).ReadToEnd();
            Trace.WriteLine(responseString);

            return Newtonsoft.Json.JsonConvert.DeserializeObject<jsonRPCResult<Dictionary<string,int>>>(responseString);
        }

        public jsonRPCResult<Dictionary<string, int>> getModels(string brand)
        {
            var dict = new Dictionary<string, string>();
            dict["brand"] = brand;
            var date = Newtonsoft.Json.JsonConvert.SerializeObject(new jsonRPCRequest { method = "cars.models", _params =  dict});
            var encodedData = Encoding.ASCII.GetBytes(date);
            var request = (HttpWebRequest)WebRequest.Create(url);
            request.ContentType = "application/json";
            request.ContentLength = encodedData.Length;
            request.Method = "POST";

            using (var stream = request.GetRequestStream())
            {
                stream.Write(encodedData, 0, encodedData.Length);
            }

            var response = (HttpWebResponse)request.GetResponse();

            var responseString = new StreamReader(response.GetResponseStream()).ReadToEnd();
            Trace.WriteLine(responseString);

            return Newtonsoft.Json.JsonConvert.DeserializeObject<jsonRPCResult<Dictionary<string, int>>>(responseString);
        }

        public jsonRPCResult<Dictionary<string, int>> getGenerations(string brand, string model)
        {
            var dict = new Dictionary<string, string>();
            dict["brand"] = brand;
            dict["model"] = model;
            var date = Newtonsoft.Json.JsonConvert.SerializeObject(new jsonRPCRequest { method = "cars.generations", _params = dict });
            var encodedData = Encoding.ASCII.GetBytes(date);
            var request = (HttpWebRequest)WebRequest.Create(url);
            request.ContentType = "application/json";
            request.ContentLength = encodedData.Length;
            request.Method = "POST";

            using (var stream = request.GetRequestStream())
            {
                stream.Write(encodedData, 0, encodedData.Length);
            }

            var response = (HttpWebResponse)request.GetResponse();

            var responseString = new StreamReader(response.GetResponseStream()).ReadToEnd();
            Trace.WriteLine(responseString);

            return Newtonsoft.Json.JsonConvert.DeserializeObject<jsonRPCResult<Dictionary<string, int>>>(responseString);
        }

        public jsonRPCResult<list_offers_result> getZeldas(string brand, string model, string generation, int priceTo)
        {
            
            var date = Newtonsoft.Json.JsonConvert.SerializeObject(new jsonRPCRequest { method = "cars.list", _params = new list_car_offers_params { brand=brand, model=model, generation = generation, price_to=priceTo} });
            var encodedData = Encoding.ASCII.GetBytes(date);
            var request = (HttpWebRequest)WebRequest.Create(url);
            request.ContentType = "application/json";
            request.ContentLength = encodedData.Length;
            request.Method = "POST";

            using (var stream = request.GetRequestStream())
            {
                stream.Write(encodedData, 0, encodedData.Length);
            }

            var response = (HttpWebResponse)request.GetResponse();

            var responseString = new StreamReader(response.GetResponseStream()).ReadToEnd();
            Trace.WriteLine(responseString);

            return Newtonsoft.Json.JsonConvert.DeserializeObject<jsonRPCResult<list_offers_result>>(responseString);
        }

        public jsonRPCResult<Dictionary<string, string>> getDetails(string link)
        {
            var dict = new Dictionary<string, string>();
            dict["link"] = link;
            var date = Newtonsoft.Json.JsonConvert.SerializeObject(new jsonRPCRequest { method = "cars.detail", _params = dict });
            var encodedData = Encoding.ASCII.GetBytes(date);
            var request = (HttpWebRequest)WebRequest.Create(url);
            request.ContentType = "application/json";
            request.ContentLength = encodedData.Length;
            request.Method = "POST";

            using (var stream = request.GetRequestStream())
            {
                stream.Write(encodedData, 0, encodedData.Length);
            }

            var response = (HttpWebResponse)request.GetResponse();

            var responseString = new StreamReader(response.GetResponseStream()).ReadToEnd();
            Trace.WriteLine(responseString);

            return Newtonsoft.Json.JsonConvert.DeserializeObject<jsonRPCResult<Dictionary<string, string>>>(responseString);
        }

        public jsonRPCResult<List<string>> getImg(string link)
        {
            var dict = new Dictionary<string, string>();
            dict["link"] = link;
            var date = Newtonsoft.Json.JsonConvert.SerializeObject(new jsonRPCRequest { method = "cars.images", _params = dict });
            var encodedData = Encoding.ASCII.GetBytes(date);
            var request = (HttpWebRequest)WebRequest.Create(url);
            request.ContentType = "application/json";
            request.ContentLength = encodedData.Length;
            request.Method = "POST";

            using (var stream = request.GetRequestStream())
            {
                stream.Write(encodedData, 0, encodedData.Length);
            }

            var response = (HttpWebResponse)request.GetResponse();

            var responseString = new StreamReader(response.GetResponseStream()).ReadToEnd();
            Trace.WriteLine(responseString);

            return Newtonsoft.Json.JsonConvert.DeserializeObject<jsonRPCResult<List<string>>>(responseString);
        }


        public void Przeglad(string link)
        {
            Process.Start("explorer.exe", link);
        }

        public jsonRPCResult<Dictionary<string, int>> getPartsBrands()
        {
            var date = Newtonsoft.Json.JsonConvert.SerializeObject(new jsonRPCRequest { method = "parts.brands", _params = new Dictionary<string, int>() });
            var encodedData = Encoding.ASCII.GetBytes(date);
            var request = (HttpWebRequest)WebRequest.Create(url);
            request.ContentType = "application/json";
            request.ContentLength = encodedData.Length;
            request.Method = "POST";

            using (var stream = request.GetRequestStream())
            {
                stream.Write(encodedData, 0, encodedData.Length);
            }

            var response = (HttpWebResponse)request.GetResponse();

            var responseString = new StreamReader(response.GetResponseStream()).ReadToEnd();
            Trace.WriteLine(responseString);

            return Newtonsoft.Json.JsonConvert.DeserializeObject<jsonRPCResult<Dictionary<string, int>>>(responseString);
        }
        public jsonRPCResult<Dictionary<string, string>> getPartsDetails(string link)
        {
            var dict = new Dictionary<string, string>();
            dict["link"] = link;
            var date = Newtonsoft.Json.JsonConvert.SerializeObject(new jsonRPCRequest { method = "parts.detail", _params = dict });
            var encodedData = Encoding.ASCII.GetBytes(date);
            var request = (HttpWebRequest)WebRequest.Create(url);
            request.ContentType = "application/json";
            request.ContentLength = encodedData.Length;
            request.Method = "POST";

            using (var stream = request.GetRequestStream())
            {
                stream.Write(encodedData, 0, encodedData.Length);
            }

            var response = (HttpWebResponse)request.GetResponse();

            var responseString = new StreamReader(response.GetResponseStream()).ReadToEnd();
            Trace.WriteLine(responseString);

            return Newtonsoft.Json.JsonConvert.DeserializeObject<jsonRPCResult<Dictionary<string, string>>>(responseString);
        }

        public jsonRPCResult<List<string>> getPartsImg(string link)
        {
            var dict = new Dictionary<string, string>();
            dict["link"] = link;
            var date = Newtonsoft.Json.JsonConvert.SerializeObject(new jsonRPCRequest { method = "parts.images", _params = dict });
            var encodedData = Encoding.ASCII.GetBytes(date);
            var request = (HttpWebRequest)WebRequest.Create(url);
            request.ContentType = "application/json";
            request.ContentLength = encodedData.Length;
            request.Method = "POST";

            using (var stream = request.GetRequestStream())
            {
                stream.Write(encodedData, 0, encodedData.Length);
            }

            var response = (HttpWebResponse)request.GetResponse();

            var responseString = new StreamReader(response.GetResponseStream()).ReadToEnd();
            Trace.WriteLine(responseString);

            return Newtonsoft.Json.JsonConvert.DeserializeObject<jsonRPCResult<List<string>>>(responseString);
        }

        public jsonRPCResult<list_offers_result> getZeldasPart(string brand, string query, int priceTo)
        {

            var date = Newtonsoft.Json.JsonConvert.SerializeObject(new jsonRPCRequest { method = "parts.query", _params = new list_part_offers_params { brand = brand, query = query, price_to = priceTo } });
            var encodedData = Encoding.ASCII.GetBytes(date);
            var request = (HttpWebRequest)WebRequest.Create(url);
            request.ContentType = "application/json";
            request.ContentLength = encodedData.Length;
            request.Method = "POST";

            using (var stream = request.GetRequestStream())
            {
                stream.Write(encodedData, 0, encodedData.Length);
            }

            var response = (HttpWebResponse)request.GetResponse();

            var responseString = new StreamReader(response.GetResponseStream()).ReadToEnd();
            Trace.WriteLine(responseString);

            return Newtonsoft.Json.JsonConvert.DeserializeObject<jsonRPCResult<list_offers_result>>(responseString);
        }

    }

    public class jsonRPCRequest
    {
        public jsonRPCRequest()
        {
            id = 0;
            jsonrpc = "2.0";
        }
        public int id { get; set; }
        public string jsonrpc { get; set; }
        public string method { get; set; }
        [Newtonsoft.Json.JsonProperty(PropertyName ="params")]
        public object _params { get; set; }

    }

    public class jsonRPCResult<T>
    {
        public int id { get; set; }
        public string jsonrpc { get; set; }
        public T result { get; set; }
    }

    public class list_car_offers_params
    {
        public string brand { get; set; }
        public string model { get; set; }
        public int price_to { get; set; }
        public int price_from { get; set; }
        public string generation { get; set; }
        public Nullable<int> page { get; set; }

        public list_car_offers_params()
        {
            price_from = 0;
            generation = null;
            page = null;
        }
    }

    public class list_offers_result
    {
        public List<string> urls { get; set; }
        public int max_page_num { get; set; }
    }

    public class list_part_offers_params
    {
        public string query { get; set; }
        public string brand { get; set; }
        public int price_to { get; set; }
        public int price_from { get; set; }
        public Nullable<int> page { get; set; }

        public list_part_offers_params()
        {
            price_from = 0;
            page = null;
        }
    }
}
