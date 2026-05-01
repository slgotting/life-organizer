export const objectToFormData = (obj) => {
    const formData = new FormData();
    for (const key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        const value = obj[key];
        formData.append(key, value);
      }
    }
    return formData;
  };
