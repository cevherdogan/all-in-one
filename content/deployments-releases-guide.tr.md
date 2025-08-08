---
title: "Deployments, Sürümler ve Dal (Branch) Stratejisi"
description: "Katkıcılar için kılavuz: deployments, sürüm notları, changelog, etiketleme ve dal (branch) stratejisi."
badges: [Rehber, Git Akışı, Sürüm Yönetimi]
slug: "deployments-releases-guide"
lang: "tr"
---

Bu kılavuz, ALL-IN-ONE projesinde **deployment geçmişi**, **sürüm notları** ve **dal/etiket (tag) stratejisini** nasıl okuyacağınızı ve uygulayacağınızı açıklar.

## 1. Deployments Nasıl Kontrol Edilir?
- Adres: [GitHub → Deployments](https://github.com/cevherdogan/all-in-one/deployments)
- Her deployment kaydında şu bilgiler yer alır:
  - **Environment** (örn. `github-pages`)
  - **Commit hash**
  - **Deployed by** (kim yayınladı)
  - **Timestamp** (zaman)
- En son içeriğin ne zaman canlıya alındığını buradan teyit edebilirsiniz.

## 2. Release Notes (Sürüm Notları)
- Sürüm notları, etiketlenmiş her sürümde nelerin değiştiğini özetler.
- Gelecekteki sürümlerde şunlar yer alacaktır:
  - **Yeni makaleler/rehberler**
  - **Şablon güncellemeleri**
  - **Otomasyon iyileştirmeleri**
- Erişim: GitHub → **Releases** sekmesi.

## 3. CHANGELOG.md
- `CHANGELOG.md`, değişiklikleri kronolojik sırayla listeler.
- Format:
  ```
  ## [vX.Y.Z] - YYYY-MM-DD
  ### Added
  - Yeni içerik veya özellik

  ### Changed
  - Mevcut sayfalarda güncellemeler

  ### Fixed
  - Hata düzeltmeleri
  ```
- Anlamlı her değişiklikte changelog’u güncellemek katkıcı sorumluluğudur.

## 4. Etiketleme (Tagging) Stratejisi
- Semantik versiyonlama: `vMAJOR.MINOR.PATCH`
  - **MAJOR**: Geriye dönük uyumsuz kırıcı değişiklikler
  - **MINOR**: Yeni içerik/özellikler
  - **PATCH**: Küçük düzeltmeler
- Örnek:
  - `v1.0.0` — ilk genel sürüm
  - `v1.1.0` — 3 yeni rehber eklendi
  - `v1.1.1` — yazım ve bağlantı düzeltmeleri

## 5. Dal (Branch) Stratejisi
- `main` **kilitlidir** — doğrudan push kapalıdır.
- Tüm değişiklikler fork’tan gelen **Pull Request**’lerle yapılır.
- Dal isimleri:
  - `feature/<kısa-açıklama>` — yeni içerik/özellik
  - `fix/<kısa-açıklama>` — hata/düzeltme
  - `docs/<kısa-açıklama>` — yalnız dokümantasyon
- PR şartları:
  - Otomatik kontrollerden geçmek
  - İnceleme ve onay almak

## 6. Neden Önemli?
- **Şeffaflık**: Ne zaman, neyin canlıya alındığı net görünür.
- **Kalite**: Eş değerlendirme (peer review) tutarlılığı artırır.
- **İzlenebilirlik**: Etiket ve changelog, sürümler arasında takibi kolaylaştırır.

## Topluluk Öğrenimi
Bu kılavuzu takip ederek yöneticiler, katkıcılar ve okuyucular kolayca:
- Yenilikleri görebilir
- İş akışını anlayabilir
- Tahmin yürütmeden projeye dahil olabilir
