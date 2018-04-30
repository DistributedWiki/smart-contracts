import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import { ArticleService } from './article.service';
import {Web3Service} from './web3.service';
import {FormsModule} from '@angular/forms';


@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    FormsModule
  ],
  providers: [ArticleService, Web3Service],
  bootstrap: [AppComponent]
})
export class AppModule { }
