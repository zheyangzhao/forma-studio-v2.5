    const count = await visibleGalleryCount(section);
    /* §A 加 evolink-ecommerce + evolink-poster 入 image sub 後，marketing+image 預期 40-60 條 */
    if (!(count > 30 && count <= 70)) {
      throw new Error(`Expected marketing/image gallery count > 30 and <= 70, got ${count}`);
    }
  });