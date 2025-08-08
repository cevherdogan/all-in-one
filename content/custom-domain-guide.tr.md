---
title: "Hostinger Üzerinden GitHub Pages Özel Alan Adı Kurulumu"
description: "all-in-one.foundral.tech alan adını GitHub Pages sitesine yönlendirme adım adım kılavuzu."
badges: [Rehber, GitHub Pages, DNS]
slug: "custom-domain-guide"
lang: "tr"
---

Bu kılavuz, **Hostinger** üzerinden yönetilen bir alan adını **GitHub Pages** sitesine bağlama sürecini, `all-in-one.foundral.tech` örneğiyle anlatır.

## 1. Ön Gereklilikler
- GitHub Pages etkin bir depo:  
  Örnek: https://github.com/cevherdogan/all-in-one  
  Varsayılan Pages adresi: https://cevherdogan.github.io/all-in-one/
- `foundral.tech` alanı için Hostinger **hPanel** erişimi.

## 2. Hostinger'da CNAME Kaydı Ekleme
1. Hostinger’a giriş yap: [DNS Zone Editor](https://hpanel.hostinger.com/domain/foundral.tech/dns)
2. **Add New Record** (Yeni Kayıt Ekle) seçeneğine tıkla.
3. Şu bilgileri gir:
   ```
   Type: CNAME
   Name: all-in-one   (@ işareti olmadan)
   Target: cevherdogan.github.io
   TTL: 3600
   ```
4. Kaydet.

## 3. GitHub Pages Ayarları
1. Depo **Settings → Pages** menüsüne git.  
2. **Custom domain** alanına şunu yaz:
   ```
   all-in-one.foundral.tech
   ```
3. “Enforce HTTPS” seçeneğini işaretle (DNS çözüldükten sonra etkinleşir).

## 4. DNS Yayılımını Bekle
- Bu işlem 15 dakika ile 24 saat arasında sürebilir.
- Doğrulamak için:  
  ```
  nslookup all-in-one.foundral.tech
  ```
  veya [whatsmydns.net](https://www.whatsmydns.net/) gibi çevrimiçi araçları kullan.

## 5. Sitenin Yayında Olduğunu Doğrula
DNS çözüldükten ve HTTPS etkinleştikten sonra siteniz şu adreste yayında olacaktır:  
**https://all-in-one.foundral.tech/**

## ✅ Örnek Yayın Günlüğü
> “Your site is live at https://all-in-one.foundral.tech/  
> Last deployed by @cevherdogan — 13 minutes ago”

## Topluluk Öğrenimi
Bu süreç, tüm katılımcıların:
- Alan adı yönlendirme temellerini öğrenmesi,
- Kendi projelerinde uygulaması,
- Bu kılavuzun farklı dil çevirilerine katkı yapması
için belgelenmiştir.
