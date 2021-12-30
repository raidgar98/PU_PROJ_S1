using System;
using System.Collections.Generic;
using System.Diagnostics;
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
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace WpfProjectPU
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        Obsluga obs = new Obsluga();
        public MainWindow()
        {
            InitializeComponent();
            var res = obs.getBrands();
            foreach(var kv in res.result.Keys)
            {
                TBMarka.Items.Add(kv);
            }
        }

        private void BTNCzWid_Click(object sender, RoutedEventArgs e)
        {
            WindowCzesci wc = new WindowCzesci();
            wc.Show();
        }

        private void Szukaj_Click(object sender, RoutedEventArgs e)
        {
            var res = obs.getZeldas(this.TBMarka.SelectedValue.ToString(), this.TBModel.SelectedValue.ToString());
            lBox.Items.Clear();
            foreach (var kv in res.result.urls)
            {
                lBox.Items.Add(kv);
            }
        }

        private void BTNSzuCz_Click(object sender, RoutedEventArgs e)
        {

        }

        private void BTNOferta_Click(object sender, RoutedEventArgs e)
        {
            obs.Przeglad();
        }

        private void TBMarka_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            var res = obs.getModels(this.TBMarka.SelectedValue.ToString());
            TBModel.Items.Clear();
            foreach (var kv in res.result.Keys)
            {
                TBModel.Items.Add(kv);
            }
        }

        private void TBModel_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            return;
            var res = obs.getGenerations(this.TBMarka.SelectedValue.ToString(),this.TBModel.SelectedValue.ToString());
            TBGeneracja.Items.Clear();
            if (res.result.Count == 0)
            {
                TBGeneracja.IsEnabled = false;
                return;
            }
            else
            {
                TBGeneracja.IsEnabled = true;
            }
            foreach (var kv in res.result.Keys)
            {
                TBGeneracja.Items.Add(kv);
            }
        }
    }
}
