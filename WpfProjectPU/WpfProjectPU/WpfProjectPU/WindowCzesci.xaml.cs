using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace WpfProjectPU
{
    /// <summary>
    /// Interaction logic for WindowCzesci.xaml
    /// </summary>
    public partial class WindowCzesci : Window
    {
        Obsluga obs = new Obsluga();
        const string wedding = "<brak wyboru>";
        list_offers_result currLi;
        bool isCleard;
        public WindowCzesci()
        {
            InitializeComponent();
            var res = obs.getPartsBrands();
            foreach (var kv in res.result.Keys)
            {
                TBMarka.Items.Add(kv);
            }
            TBMarka.Items.Add(wedding);
        }

        private void BTNSamWid_Click(object sender, RoutedEventArgs e)
        {
            MainWindow mw = new MainWindow();
            mw.Show();
            this.Close();
        }

        private void Szukaj_Click(object sender, RoutedEventArgs e)
        {
            string chMarka = this.TBMarka.SelectedValue.ToString();
            string chPrice = this.TBPrice.Text;
            currLi = obs.getZeldasPart((chMarka == wedding ? null:chMarka), this.TBRodzaj.Text, (chPrice == "" ? 900000:Int32.Parse(chPrice))).result;
            lBox.Items.Clear();
            foreach (var item in currLi.urls)
            {
                string kv = item.Remove(0, item.LastIndexOf('/') + 1);
                kv = kv.Remove(kv.LastIndexOf('-'), kv.Length - kv.LastIndexOf('-'));
                kv = kv.Replace('-', ' ');
                lBox.Items.Add(kv);
            }
        }


        private void BTNOferta_Click(object sender, RoutedEventArgs e)
        {
            if (lBox.SelectedIndex != -1)
            {
                var res = currLi.urls[lBox.SelectedIndex];
                obs.Przeglad(res);
            }
        }

        private void lBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (lBox.SelectedIndex != -1)
            {
                var res = obs.getPartsDetails(currLi.urls[lBox.SelectedIndex]);
                TB1.Text = res.result["Oferta od"];
                TB2.Text = res.result["Stan"];
                TB3.Text = res.result["Marka pojazdu"];
                TB4.Text = res.result["Kategoria części"];

                var res2 = obs.getImg(currLi.urls[lBox.SelectedIndex]);
                if (res2.result.Count > 0)
                {
                    img.BeginInit();
                    img.Source = new BitmapImage(new Uri(res2.result[0]));
                    img.EndInit();
                }
            }
        }
    }
}
