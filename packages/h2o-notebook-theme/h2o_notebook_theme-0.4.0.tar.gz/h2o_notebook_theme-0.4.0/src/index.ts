import type { IPlugin } from '@lumino/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * This is hacky, but it works. I did not find a way how to load a static file from the Jupyter extension. But I use the
 * favicon SVG in CSS and CSS files are loaded through Webpack and uses url-loader. The Webpack loader do not work in
 * this file, it seems it only runs for the `../style` directory. I'm inexperienced with the Jupyter build system, but I
 * know Webpack, so I overrided the loader in CSS to not inline the logo as Base64 and not change the name of the logo,
 * so I can reference it here.
 * TLDR; the CSS loads the file and this function uses loosely path to the file on the server, it is fragile, but works.
 */
const replaceFavicon = () => {
  const favicon = document.head.querySelector(
    'link[rel=icon]'
  ) as HTMLLinkElement;
  favicon.href = 'lab/api/themes/h2o-notebook-theme/logo.svg';
  favicon.type = 'image/svg+xml';
};

const changeTitle = () => {
  document.title = 'Notebook Lab | H2O AI Cloud';
  // The Jupyter changes the title once in the while, to prevent that, we make
  // the title read-only 👅
  Object.defineProperty(document, 'title', {
    writable: false,
  });
};

/**
 * Initialization data for the h2o-notebook-theme extension.
 */
const extension: IPlugin<any, void> = {
  id: 'h2o-notebook-theme',
  requires: [IThemeManager],
  autoStart: true,
  activate: (app: any, manager: IThemeManager) => {
    const style = 'h2o-notebook-theme/index.css';
    manager.register({
      name: 'H2O',
      isLight: false,
      load: () => {
        changeTitle();
        replaceFavicon();
        return manager.loadCSS(style);
      },
      unload: () => Promise.resolve(),
    });
  },
};

export default extension;
