﻿using System;
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
        list_car_offers_result currLi;
        bool isCleard;
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
            currLi = obs.getZeldas(this.TBMarka.SelectedValue.ToString(), this.TBModel.SelectedValue.ToString()).result;
            lBox.Items.Clear();
            foreach (var item in currLi.urls)
            {
                //https://www.otomoto.pl/oferta/opel-astra-opel-astra-1-7-cdti-ID6Elx4V.html
                //tmp.LastIndexOf
                string kv = item.Remove(0, item.LastIndexOf('/')+1);
                kv = kv.Remove(kv.LastIndexOf('-'),kv.Length-kv.LastIndexOf('-'));
                kv = kv.Replace('-', ' ');
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
            isCleard = true;
            TBGeneracja.Items.Clear();
            TBModel.Items.Clear();
            isCleard = false;
            var res = obs.getModels(this.TBMarka.SelectedValue.ToString());
            
            foreach (var kv in res.result.Keys)
            {
                TBModel.Items.Add(kv);
            }
        }

        private void TBModel_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (isCleard) return;
            TBGeneracja.Items.Clear();
            var res = obs.getGenerations(this.TBMarka.SelectedValue.ToString(),this.TBModel.SelectedValue.ToString());
            
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

        private void lBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (lBox.SelectedIndex != -1)
            {
                var res = obs.getDetails(currLi.urls[lBox.SelectedIndex]);
                TB1.Text = res.result["Rok produkcji"];
                TB2.Text = res.result["Przebieg"];
                TB3.Text = res.result["Pojemność skokowa"];
                TB4.Text = res.result["Rodzaj paliwa"];

                var res2 = obs.getImg(currLi.urls[lBox.SelectedIndex]);
                img.BeginInit();
                img.Source = new BitmapImage(new Uri(res2.result[0]));
                img.EndInit();
            }
            
        }
    }
}
