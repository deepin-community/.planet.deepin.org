/*
 * SPDX-FileCopyrightText: 2021-2022 Phu Hung Nguyen <phu.nguyen@kdemail.net>
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

const navPosts = (delta) => {
  const posts = document.querySelectorAll('div.single-post');

  if (delta > 0) {
    let i = 0;
    for (; i < posts.length; i++) {
      let topPos = posts[i].getBoundingClientRect().top;
      if (Math.abs(topPos) < 1) topPos = 0;
      if (topPos > 0) {
        posts[i].scrollIntoView({behavior: 'smooth'});
        return;
      }
    }
    if (i >= posts.length)
      posts[posts.length-1].scrollIntoView({behavior: 'smooth', block: "end"});
  } else {
    for (let i = posts.length - 1; i >= 0; i--) {
      let topPos = posts[i].getBoundingClientRect().top;
      if (Math.abs(topPos) < 1) topPos = 0;
      if (topPos < 0) {
        posts[i].scrollIntoView({behavior: 'smooth'});
        return;
      }
    }
  }
}
